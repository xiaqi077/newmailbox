import asyncio
import logging
from typing import List
from datetime import datetime

from app.models.email_account import EmailAccount
from app.services.sync_helpers import AsyncSessionLocal
from app.services.imap_sync import sync_emails

logger = logging.getLogger(__name__)

SYNC_INTERVAL_SECONDS = 15  # 每15秒同步一次

class SyncScheduler:
    """后台同步调度器"""
    
    def __init__(self):
        self._task = None
        self._running = False
    
    async def start(self):
        """启动调度器"""
        if self._task is not None:
            return
        
        self._running = True
        self._task = asyncio.create_task(self._run_loop())
        logger.info(f"Sync scheduler started with interval {SYNC_INTERVAL_SECONDS}s")
    
    async def stop(self):
        """停止调度器"""
        self._running = False
        if self._task is not None:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None
        logger.info("Sync scheduler stopped")
    
    async def _run_loop(self):
        """主循环"""
        while self._running:
            try:
                await self._sync_all_accounts()
            except Exception as e:
                logger.error(f"Error in sync loop: {e}", exc_info=True)
            
            # 等待下一个周期
            await asyncio.sleep(SYNC_INTERVAL_SECONDS)
    
    async def _sync_all_accounts(self):
        """同步所有启用同步的账号"""
        from sqlalchemy import select
        
        async with AsyncSessionLocal() as db:
            try:
                # 获取所有启用同步的账号
                result = await db.execute(
                    select(EmailAccount).where(
                        EmailAccount.sync_enabled == True,
                        EmailAccount.is_active == True
                    )
                )
                accounts = result.scalars().all()
                
                if not accounts:
                    return
                
                logger.debug(f"Found {len(accounts)} accounts to sync")
                
                # 逐个同步
                for account in accounts:
                    try:
                        # 检查距离上次同步是否已经过了足够时间
                        if account.last_sync_at:
                            time_since_sync = (datetime.utcnow() - account.last_sync_at).total_seconds()
                            if time_since_sync < SYNC_INTERVAL_SECONDS:
                                continue  # 跳过，还没到时间
                        
                        logger.info(f"Syncing account {account.email_address}")
                        await sync_emails(account.id, db, limit=100)
                        
                    except Exception as e:
                        logger.error(f"Error syncing account {account.id}: {e}", exc_info=True)
                
                await db.commit()
                
            except Exception as e:
                await db.rollback()
                logger.error(f"Error in sync_all_accounts: {e}", exc_info=True)


# 全局实例
scheduler = SyncScheduler()


async def start_scheduler():
    """启动调度器（用于应用启动时调用）"""
    await scheduler.start()


async def stop_scheduler():
    """停止调度器（用于应用关闭时调用）"""
    await scheduler.stop()
