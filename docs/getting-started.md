# Getting Started

This guide will walk you through the basics of using `building_blocks` to create a simple, clean application.

## 1. Installation

First, install the library using Poetry or pip:

```bash
# With Poetry
poetry add building-blocks

# With pip
pip install building-blocks
```

## 2. Define a Domain Entity

Let's start by defining a simple domain entity. An entity is a core object in your business domain.

```python name=src/my_app/domain/entities.py
from dataclasses import dataclass

@dataclass
class User:
    id: int
    name: str
    email: str
```

## 3. Define an Outbound Port (Repository)

Next, define an interface (an outbound port) for how the application will fetch user data. This will be an abstract base class.

```python name=src/my_app/application/ports/user_repository.py
from abc import ABC, abstractmethod
from typing import Optional
from my_app.domain.entities import User

class UserRepository(ABC):

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        ...

    @abstractmethod
    def save(self, user: User) -> None:
        ...
```

## 4. Create an Application Service (Use Case)

Now, create an application service that defines a use case for your application, like fetching a user.

```python name=src/my_app/application/services.py
from my_app.application.ports.user_repository import UserRepository
from my_app.domain.entities import User

class UserService:

    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def get_user(self, user_id: int) -> Optional[User]:
        return self._user_repository.get_by_id(user_id)
```

## 5. Implement an Adapter

Now, you can create a concrete implementation (an adapter) for your repository. For example, an in-memory repository for testing.

```python name=src/my_app/infrastructure/repositories/in_memory_user_repository.py
from typing import Optional
from my_app.application.ports.user_repository import UserRepository
from my_app.domain.entities import User

class InMemoryUserRepository(UserRepository):
    _users: dict[int, User] = {}

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self._users.get(user_id)

    def save(self, user: User) -> None:
        self._users[user.id] = user
```

## 6. Wire It All Up

Finally, in your application's entry point (e.g., a `main.py` or a web server's startup script), you can wire everything together.

```python name=main.py
from my_app.application.services import UserService
from my_app.infrastructure.repositories.in_memory_user_repository import InMemoryUserRepository
from my_app.domain.entities import User

# Create instances
user_repo = InMemoryUserRepository()
user_service = UserService(user_repository=user_repo)

# Use the service
new_user = User(id=1, name="John Doe", email="john.doe@example.com")
user_repo.save(new_user)

retrieved_user = user_service.get_user(1)
print(retrieved_user)
```

This example shows how the layers are decoupled. The `UserService` depends on the `UserRepository` interface, not the concrete `InMemoryUserRepository`. This makes it easy to swap implementations without changing the application logic.
