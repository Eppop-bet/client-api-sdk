from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any
from datetime import datetime


class Sport(BaseModel):
    id: int
    name: str
    slug: str


class Player(BaseModel):
    player_id: int = Field(alias="playerId")
    name: str
    first_name: Optional[str] = Field(default=None, alias="firstName")
    last_name: Optional[str] = Field(default=None, alias="lastName")
    active: bool = Field(default=True)
    age: Optional[int] = None
    birthday: Optional[datetime] = None
    image_url: Optional[str] = Field(default=None, alias="imageUrl")
    modified_at: datetime = Field(alias="modifiedAt")
    nationality: Optional[str] = None
    role: Optional[str] = None
    slug: str


class Team(BaseModel):
    team_id: int = Field(alias="teamId")
    name: str
    slug: str
    acronym: Optional[str] = None
    image_url: Optional[str] = Field(default=None, alias="imageUrl")
    location: Optional[str] = None
    modified_at: datetime = Field(alias="modifiedAt")


class TeamWithPlayers(Team):
    players: List[Player]


class Map(BaseModel):
    map_id: int = Field(alias="mapId")
    name: str
    slug: str


class TradingCategory(BaseModel):
    id: int
    name: str
    sport_id: int = Field(alias="sportId")


class TradingTournament(BaseModel):
    id: int
    name: str
    sport_id: int = Field(alias="sportId")
    trading_category_id: Optional[int] = Field(default=None, alias="tradingCategoryId")


class TradingOutcome(BaseModel):
    id: int
    name: str
    trading_market_id: int = Field(alias="tradingMarketId")
    status: Literal["Unknown", "Win", "Lose", "Return", "Return025", "Return075"]
    result: Literal["Unknown", "Win", "Lose", "Return", "Return025", "Return075"]
    score: Optional[int] = None
    price: float
    probability: float


class TradingMarket(BaseModel):
    id: int
    status: str
    event_id: int = Field(alias="eventId")
    period: Literal["Map1", "Map2", "Match"]
    competitor_ids: List[int] = Field(alias="competitorIds")
    competitor_type: Literal["Player", "Team"] = Field(alias="competitorType")
    market_key: Literal["H2H", "UnderOver"] = Field(alias="marketKey")
    value: Optional[float] = None
    outcomes: List[TradingOutcome]


class TradingEvent(BaseModel):
    id: int
    name: str
    sport_id: int = Field(alias="sportId")
    sport: Sport
    status: Literal["Review", "Open", "Suspended", "ResultAwaiting", "Resulted", "Corrected"]
    begin_at: datetime = Field(alias="beginAt")
    modified_at: datetime = Field(alias="modifiedAt")
    archived: bool
    notes: Optional[str] = None
    competitor_type: Literal["Player", "Team"] = Field(alias="competitorType")
    competitor_ids: List[int] = Field(alias="competitorIds")
    trading_markets: List[TradingMarket] = Field(alias="tradingMarkets")


class ChangeLog(BaseModel):
    id: int
    table_name: str = Field(alias="tableName")
    record_id: int = Field(alias="recordId")
    added_at: datetime = Field(alias="addedAt")
    data: Dict[str, Any]
    action: Literal["CREATE", "UPDATE", "DELETE"]


class SignInResponse(BaseModel):
    access_token: str = Field(alias="AccessToken")
    expires_in: int = Field(alias="ExpiresIn")
