from unittest import mock
from unittest.mock import AsyncMock, Mock

import pytest

from taskflow_primitives.application.ports.inbound.create_task_use_case import (
    CreateTaskRequest,
)
from taskflow_primitives.application.services.create_task_service import (
    CreateTaskService,
)
from taskflow_primitives.domain.ports.outbound.task_repository import TaskRepository


class TestCreateTaskService:
    @pytest.mark.asyncio
    async def test_create_task(self):
        uuid4_result = "1234567890abcdef"

        with mock.patch("taskflow_primitives.domain.entities.task.uuid4") as MockUUID4:
            MockUUID4.return_value.hex = uuid4_result
            mock_repo = Mock(spec=TaskRepository)
            mock_repo.save = AsyncMock()
            create_task_service = CreateTaskService(mock_repo)

            response = await create_task_service.execute(
                CreateTaskRequest(
                    title="Test Task",
                    description="This is a test task.",
                    due_date="2023-10-01",
                    priority=1,
                )
            )

            assert response.task_id == uuid4_result
