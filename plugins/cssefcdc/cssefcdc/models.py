from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship
from cssefserver.modelbase import BASE as Base
from cssefserver.modelutils import get_foreign_key
from cssefserver.account.models import Organization

class Competition(Base):
    organization = Column(Integer, get_foreign_key(Organization))
    #scoringEngine = relationship('ScoringEngine')
    teams = relationship('Team')
    scores = relationship('Score')
    injects = relationship('Inject')
    injectResponses = relationship('InjectResponse')
    incidents = relationship('Incident')
    incidentResponses = relationship('IncidentResponse')
    name = Column(String(50))
    url = Column(String(50))
    description = Column(String(1000))
    datetimeDisplay = Column(DateTime)
    datetimeStart = Column(DateTime)
    datetimeFinish = Column(DateTime)
    autoStart = Column(Boolean)
    # scoringInterval = PositiveIntegerField(null = True)
    # scoringIntervalUncertainty = PositiveIntegerField(null = True)
    # scoringMethod = CharField(max_length = 20, null = True, blank = True)    # set to either CIDR or domain name
    # scoringSlaEnabled = BooleanField(default = True)
    # scoringSlaThreashold = PositiveIntegerField(null = True)
    # scoringSlaPenalty = PositiveIntegerField(null = True)
    # servicesEnabled = BooleanField(default = True)

    # These are all related specifically to the Web Interface.
    # These should be moved over to a model for configuring the
    # web interface rather than the competition
    teamsViewRankingEnabled = Column(Boolean)
    teamsViewScoreboardEnabled = Column(Boolean)
    teamsViewServiceStatisticsEnabled = Column(Boolean)
    teamsViewServiceStatusEnabled = Column(Boolean)
    teamsViewInjectsEnabled = Column(Boolean)
    teamsViewIncidentResponseEnabled = Column(Boolean)

class Team(Base):
    competition = Column(Integer, get_foreign_key(Competition))
    scores = relationship('Score')
    last_login = Column(DateTime)
    name = Column(String(30))
    username = Column(String(30))
    password = Column(String(64))
    networkCidr = Column(String(30))
    scoreConfigurations = Column(String(1000))

class Score(Base):
    competition = Column(Integer, get_foreign_key(Competition))
    team = Column(Integer, get_foreign_key(Team))
    datetime = Column(DateTime)
    value = Column(Integer)
    message = Column(String(100))

class Inject(Base):
    competition = Column(Integer, get_foreign_key(Competition))
    title = Column(String(50))
    body = Column(String(1000))
    responses = relationship('InjectResponse')
    requireResponse = Column(Boolean, default=True)
    manualDelivery = Column(Boolean, default=False)
    datetimeDelivery = Column(DateTime, nullable=True, default=None)
    datetimeResponseDue = Column(DateTime, nullable=True, default=None)
    datetimeResponseClose = Column(DateTime, nullable=True, default=None)

class InjectResponse(Base):
    competition = Column(Integer, get_foreign_key(Competition))
    team = Column(Integer, get_foreign_key(Team))
    inject = Column(Integer, get_foreign_key(Inject))
    datetime = Column(DateTime)
    content = Column(String(20))

class Incident(Base):
    competition = Column(Integer, get_foreign_key(Competition))
    team = Column(Integer, get_foreign_key(Team))
    datetime = Column(DateTime)
    subject = Column(String(100))
    content = Column(String(1000))

class IncidentResponse(Base):
    competition = Column(Integer, get_foreign_key(Competition))
    team = Column(Integer, get_foreign_key(Team))
    incident = Column(Integer, get_foreign_key(Incident))
    #replyTo = Column(Integer, get_foreign_key(IncidentResponse))
    #replies = relationship('IncidentResponse')
    datetime = Column(DateTime)
    subject = Column(String(100))
    content = Column(String(1000))

class ScoringEngine(Base):
    name = Column(String(256))
    packageName = Column(String(256))
    enabled = Column(Boolean, default=True)

class Plugin(Base):
    name = Column(String(20))
    description = Column(String(256))

class Service(Base):
    competition = Column(Integer, get_foreign_key(Competition))
    plugin = Column(Integer, get_foreign_key(Plugin))
    name = Column(String(20))
    description = Column(String(256))
    manualStart = Column(Boolean, default=True)
    datetimeStart = Column(DateTime)
    datetimeFinish = Column(DateTime)
    points = Column(Integer)
    machineIp = Column(String(15))
    machineFqdn = Column(String(50))
    defaultPort = Column(Integer)
