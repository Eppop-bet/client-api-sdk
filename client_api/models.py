from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any
from datetime import datetime


class Sport(BaseModel):
    id: int
    name: str
    slug: str


class Player(BaseModel):
    playerId: int
    name: str
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    active: bool = Field(default=True)
    age: Optional[int] = None
    birthday: Optional[datetime] = None
    imageUrl: Optional[str] = None
    modifiedAt: datetime
    nationality: Optional[str] = None
    role: Optional[str] = None
    slug: str


class Team(BaseModel):
    teamId: int
    name: str
    slug: str
    acronym: Optional[str] = None
    imageUrl: Optional[str] = None
    location: Optional[str] = None
    modifiedAt: datetime


class TeamWithPlayers(Team):
    players: List[Player]


class Map(BaseModel):
    mapId: int
    name: str
    slug: str


class TradingCategory(BaseModel):
    id: int
    name: str
    sportId: int


class TradingTournament(BaseModel):
    id: int
    name: str
    sportId: int
    tradingCategoryId: Optional[int] = None


class TradingOutcome(BaseModel):
    id: int
    name: str
    tradingMarketId: int
    status: Literal["Unknown", "Win", "Lose", "Return", "Return025", "Return075"]
    result: Literal["Unknown", "Win", "Lose", "Return", "Return025", "Return075"]
    score: Optional[int] = None
    price: float
    probability: float


class TradingMarket(BaseModel):
    id: int
    status: str
    eventId: int
    period: Literal["Map1", "Map2", "Match"]
    competitorIds: List[int]
    competitorType: Literal["Player", "Team"]
    marketKey: Literal["H2H", "UnderOver"]
    value: Optional[float] = None
    outcomes: List[TradingOutcome]


class TradingEvent(BaseModel):
    id: int
    name: str
    sportId: int
    sport: Sport
    status: Literal["Review", "Open", "Suspended", "ResultAwaiting", "Resulted", "Corrected"]
    beginAt: datetime
    modifiedAt: datetime
    archived: bool
    notes: Optional[str] = None
    competitorType: Literal["Player", "Team"]
    competitorIds: List[int]
    tradingMarkets: List[TradingMarket]


class ChangeLog(BaseModel):
    id: int
    tableName: str
    recordId: int
    addedAt: datetime
    data: Dict[str, Any]
    action: Literal["CREATE", "UPDATE", "DELETE"]


class SignInResponse(BaseModel):
    access_token: str = Field(alias="AccessToken")
    expires_in: int = Field(alias="ExpiresIn")
