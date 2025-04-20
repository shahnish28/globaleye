from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """Simple MongoDB connection settings for internal Kubernetes/Docker networks."""

    MONGO_HOST: str = Field("localhost", description="MongoDB host")
    MONGO_PORT: int = Field(27017, description="MongoDB port")
    MONGO_DB_NAME: str = Field("gei-scraper", description="MongoDB database name")

    @property
    def MONGODB_URI(self) -> str:
        """Construct simple MongoDB connection URI."""
        return f"mongodb://{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DB_NAME}"

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
