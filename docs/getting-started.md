# Getting Started

Follow these steps to build an app with `building-blocks`.

## 1. Install

```bash
# With Poetry
poetry add building-blocks

# With pip
pip install building-blocks
```

## 2. Define a Domain Entity

```python
from dataclasses import dataclass

@dataclass
class User:
    id: int
    name: str
    email: str
```

## 3. Define an Outbound Port (Repository)

```python
from abc import ABC, abstractmethod
from typing import Optional

from building_blocks.domain.entity import User

class UserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        ...
    @abstractmethod
    def save(self, user: User) -> None:
        ...
```

## 4. Create an Application Service (Use Case)

```python
from typing import Optional

from building_blocks.application.ports.outbound.repository import UserRepository
from building_blocks.application.ports.inbound.use_case import AsyncUseCase, SyncUseCase

@dataclass
class GetUserRequest:
    user_id: int

@dataclass
class GetUserResponse:
    name: str
    email: str


class UserService:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def get_user(self, user_id: int) -> Optional[User]:
        return self._user_repository.get_by_id(user_id)
```

## 5. Implement an Adapter

```python
from typing import Optional

from building_blocks.domain.entity import User
from building_blocks.application.ports.outbound.repository import UserRepository

class InMemoryUserRepository(UserRepository):
    _users: dict[int, User] = {}

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self._users.get(user_id)

    def save(self, user: User) -> None:
        self._users[user.id] = user
```

## 6. Wire It Up

```python
from building_blocks.domain.entity import User
from building_blocks.application.services.user_service import UserService
from building_blocks.adapters.in_memory_user_repository import InMemoryUserRepository

user_repo = InMemoryUserRepository()
user_service = UserService(user_repository=user_repo)

new_user = User(id=1, name="John Doe", email="john.doe@example.com")
user_repo.save(new_user)

retrieved_user = user_service.get_user(1)
print(retrieved_user)
```

---

This structure lets you swap infra, test business logic, and scale to larger apps!
