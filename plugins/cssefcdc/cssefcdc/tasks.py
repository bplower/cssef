from cssefserver.utils import CssefRPCEndpoint
from cssefserver.utils import EndpointOutput
from cssefserver.taskutils import model_del
from cssefserver.taskutils import model_set
from cssefserver.taskutils import model_get
from cssefserver.account.utils import authorize_access
from cssefcdc.api import Competition
from cssefcdc.api import Team
from cssefcdc.api import Score
from cssefcdc.api import Inject
from cssefcdc.api import InjectResponse
from cssefcdc.api import Incident
from cssefcdc.api import IncidentResponse
from cssefcdc.api import ScoringEngine

# ==================================================
# Competition Endpoints
# ==================================================
class CompetitionAdd(CssefRPCEndpoint):
    name = "Competition Add"
    rpc_name = "competitionadd"
    menu_path = "competition.add"
    on_request_args = ['auth']
    def on_request(self, auth, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        competition = Competition.from_dict(self.database_connection, kwargs)
        content = competition.as_dict()
        return EndpointOutput(content = content)

class CompetitionDel(CssefRPCEndpoint):
    name = "Competition Delete"
    rpc_name = "competitiondel"
    menu_path = "competition.del"
    takes_kwargs = False
    on_request_args = ['auth', 'pkid']
    def on_request(self, auth, pkid):
        authorize_access(self.database_connection, auth, self.config)
        return model_del(Competition, self.database_connection, pkid)

class CompetitionSet(CssefRPCEndpoint):
    name = "Competition Set"
    rpc_name = "competitionset"
    menu_path = "competition.set"
    on_request_args = ['auth', 'pkid']
    def on_request(self, auth, pkid, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        return model_set(Competition, self.database_connection, pkid, **kwargs)

class CompetitionGet(CssefRPCEndpoint):
    name = "Competition Get"
    rpc_name = "competitionget"
    menu_path = "competition.get"
    on_request_args = ['auth']
    def on_request(self, auth, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        return model_get(Competition, self.database_connection, **kwargs)

class CompetitionStart(CssefRPCEndpoint):
    name = "Competition Start"
    rpc_name = "competitionstart"
    menu_path = "competition.start"
    takes_kwargs = False
    on_request_args = ['auth', 'pkid']
    def on_request(self, auth, pkid):
        authorize_access(self.database_connection, auth, self.config)
        competition = Competition.from_database(self.database_connection, pkid)
        competition.start()
        return EndpointOutput()

# ==================================================
# Team Endpoints
# ==================================================
class TeamAdd(CssefRPCEndpoint):
    name = "Team Add"
    rpc_name = "teamadd"
    menu_path = "team.add"
    on_request_args = ['auth', 'competition']
    def on_request(self, auth, competition, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        competition_obj = Competition.from_database(self.database_connection, competition)
        kwargs['competition'] = competition_obj.get_id()
        team = Team.from_dict(self.database_connection, kwargs)
        content = [team.as_dict()]
        return EndpointOutput(content = content)

class TeamDel(CssefRPCEndpoint):
    name = "Team Delete"
    rpc_name = "teamdel"
    menu_path = "team.del"
    takes_kwargs = False
    on_request_args = ['auth', 'competition', 'pkid']
    def on_request(self, auth, competition, pkid):
        authorize_access(self.database_connection, auth, self.config)
        return model_del(Team, self.database_connection, pkid)

class TeamSet(CssefRPCEndpoint):
    name = "Team Set"
    rpc_name = "teamset"
    menu_path = "team.set"
    on_request_args = ['auth', 'competition', 'pkid']
    def on_request(self, auth, competition, pkid, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        return model_set(Team, self.database_connection, pkid, **kwargs)

class TeamGet(CssefRPCEndpoint):
    name = "Team Get"
    rpc_name = "teamget"
    menu_path = "team.get"
    on_request_args = ['auth', 'competition']
    def on_request(self, auth, competition, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        return model_get(Team, self.database_connection, **kwargs)

# ==================================================
# Score Endpoints
# ==================================================
class ScoreAdd(CssefRPCEndpoint):
    name = "Score Add"
    rpc_name = "scoreadd"
    menu_path = "score.add"
    on_request_args = ['auth', 'competition']
    def on_request(self, auth, competition, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        competition_obj = Competition.from_database(self.database_connection, competition)
        kwargs['competition'] = competition_obj.get_id()
        score = Score.from_dict(self.database_connection, kwargs)
        content = [score.as_dict()]
        return EndpointOutput(content = content)

class ScoreDel(CssefRPCEndpoint):
    name = "Score Delete"
    rpc_name = "scoredel"
    menu_path = "score.del"
    takes_kwargs = False
    on_request_args = ['auth', 'competition', 'pkid']
    def on_request(self, auth, competition, pkid):
        authorize_access(self.database_connection, auth, self.config)
        return model_del(Score, self.database_connection, pkid)

class ScoreSet(CssefRPCEndpoint):
    name = "Score Set"
    rpc_name = "scoreset"
    menu_path = "score.set"
    on_request_args = ['auth', 'competition', 'pkid']
    def on_request(self, auth, competition, pkid, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        return model_set(Score, self.database_connection, pkid, **kwargs)

class ScoreGet(CssefRPCEndpoint):
    name = "Score Get"
    rpc_name = "scoreget"
    menu_path = "score.get"
    on_request_args = ['auth', 'competition']
    def on_request(self, auth, competition, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        return model_get(Score, self.database_connection, **kwargs)

# ==================================================
# Inject Endpoints
# ==================================================
class InjectAdd(CssefRPCEndpoint):
    name = "Inject Add"
    rpc_name = "injectadd"
    menu_path = "inject.add"
    on_request_args = ['auth', 'competition']
    def on_request(self, auth, competition, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        competition_obj = Competition.from_database(self.database_connection, competition)
        kwargs['competition'] = competition_obj.get_id()
        inject = Inject.from_dict(self.database_connection, kwargs)
        content = [inject.as_dict()]
        return EndpointOutput(content = content)

class InjectDel(CssefRPCEndpoint):
    name = "Inject Delete"
    rpc_name = "injectdel"
    menu_path = "inject.del"
    takes_kwargs = False
    on_request_args = ['auth', 'competition', 'pkid']
    def on_request(self, auth, competition, pkid):
        authorize_access(self.database_connection, auth, self.config)
        return model_del(Inject, self.database_connection, pkid)

class InjectSet(CssefRPCEndpoint):
    name = "Inject Set"
    rpc_name = "injectset"
    menu_path = "inject.set"
    on_request_args = ['auth', 'competition', 'pkid']
    def on_request(self, auth, competition, pkid, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        return model_set(Inject, self.database_connection, pkid, **kwargs)

class InjectGet(CssefRPCEndpoint):
    name = "Inject Get"
    rpc_name = "injectget"
    menu_path = "inject.get"
    on_request_args = ['auth', 'competition']
    def on_request(self, auth, competition, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        return model_get(Inject, self.database_connection, **kwargs)

# ==================================================
# Inject Response Endpoints
# ==================================================
class InjectResponseAdd(CssefRPCEndpoint):
    name = "Inject Response Add"
    rpc_name = "injectresponseadd"
    menu_path = "injectresponse.add"
    on_request_args = ['auth', 'competition']
    def on_request(self, auth, competition, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        competition_obj = Competition.from_database(self.database_connection, competition)
        kwargs['competition'] = competition_obj.get_id()
        injectResponse = InjectResponse.from_dict(self.database_connection, kwargs)
        content = [injectResponse.as_dict()]
        return EndpointOutput(content = content)

class InjectResponseDel(CssefRPCEndpoint):
    name = "Inject Response Delete"
    rpc_name = "injectresponsedel"
    menu_path = "injectresponse.del"
    takes_kwargs = False
    on_request_args = ['auth', 'competition', 'pkid']
    def on_request(self, auth, competition, pkid):
        authorize_access(self.database_connection, auth, self.config)
        return model_del(InjectResponse, self.database_connection, pkid)

class InjectResponseSet(CssefRPCEndpoint):
    name = "Inject Response Set"
    rpc_name = "injectresponseset"
    menu_path = "injectresponse.set"
    on_request_args = ['auth', 'competition', 'pkid']
    def on_request(self, auth, competition, pkid, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        return model_set(InjectResponse, self.database_connection, pkid, **kwargs)

class InjectResponseGet(CssefRPCEndpoint):
    name = "Inject Response Get"
    rpc_name = "injectresponseget"
    menu_path = "injectresponse.get"
    on_request_args = ['auth', 'competition']
    def on_request(self, auth, competition, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        return model_get(InjectResponse, self.database_connection, **kwargs)

# ==================================================
# Incident Endpoints
# ==================================================
class IncidentAdd(CssefRPCEndpoint):
    name = "Incident Add"
    rpc_name = "incidentadd"
    menu_path = "incident.add"
    on_request_args = ['auth', 'competition']
    def on_request(self, auth, competition, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        competition_obj = Competition.from_database(self.database_connection, competition)
        kwargs['competition'] = competition_obj.get_id()
        incident = Incident.from_dict(self.database_connection, kwargs)
        content = [incident.as_dict()]
        return EndpointOutput(content = content)

class IncidentDel(CssefRPCEndpoint):
    name = "Incident Del"
    rpc_name = "incidentdel"
    menu_path = "incident.del"
    takes_kwargs = False
    on_request_args = ['auth', 'competition', 'pkid']
    def on_request(self, auth, competition, pkid):
        authorize_access(self.database_connection, auth, self.config)
        return model_del(Incident, self.database_connection, pkid)

class IncidentSet(CssefRPCEndpoint):
    name = "Incident Set"
    rpc_name = "incidentset"
    menu_path = "incident.set"
    on_request_args = ['auth', 'competition', 'pkid']
    def on_request(self, auth, competition, pkid, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        return model_set(Incident, self.database_connection, pkid, **kwargs)

class IncidentGet(CssefRPCEndpoint):
    name = "Incident Get"
    rpc_name = "incidentget"
    menu_path = "incident.get"
    on_request_args = ['auth', 'competition']
    def on_request(self, auth, competition, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        return model_get(Incident, self.database_connection, **kwargs)

# ==================================================
# Incident Response Endpoints
# ==================================================
class IncidentResponseAdd(CssefRPCEndpoint):
    name = "Incident Response Add"
    rpc_name = "incidentresponseadd"
    menu_path = "incidentresponse.add"
    on_request_args = ['auth', 'competition']
    def on_request(self, auth, competition, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        competition_obj = Competition.from_database(self.database_connection, competition)
        kwargs['competition'] = competition_obj.get_id()
        incident_response = IncidentResponse.from_dict(self.database_connection, kwargs)
        content = [incident_response.as_dict()]
        return EndpointOutput(content = content)

class IncidentResponseDel(CssefRPCEndpoint):
    name = "Incident Response Delete"
    rpc_name = "incidentresponsedel"
    menu_path = "incidentresponse.del"
    takes_kwargs = False
    on_request_args = ['auth', 'competition', 'pkid']
    def on_request(self, auth, competition, pkid):
        authorize_access(self.database_connection, auth, self.config)
        return model_del(IncidentResponse, self.database_connection, pkid)

class IncidentResponseSet(CssefRPCEndpoint):
    name = "Incident Response Set"
    rpc_name = "incidentresponseset"
    menu_path = "incidentresponse.set"
    on_request_args = ['auth', 'competition', 'pkid']
    def on_request(self, auth, competition, pkid, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        return model_del(IncidentResponse, self.database_connection, pkid)

class IncidentResponseGet(CssefRPCEndpoint):
    name = "Incident Response Get"
    rpc_name = "incidentresponseget"
    menu_path = "incidentresponse.get"
    on_request_args = ['auth', 'competition']
    def on_request(self, auth, competition, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        return model_get(IncidentResponse, self.database_connection, **kwargs)

# ==================================================
# Scoring Engine Endpoints
# ==================================================
class ScoringEngineAdd(CssefRPCEndpoint):
    name = "Scoring Engine Add"
    rpc_name = "scoringengineadd"
    menu_path = "scoringengine.add"
    on_request_args = ['auth']
    def on_request(self, auth, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        scoringEngine = ScoringEngine.from_dict(self.database_connection, kwargs)
        content = [scoringEngine.as_dict()]
        return EndpointOutput(content = content)

class ScoringEngineDel(CssefRPCEndpoint):
    name = "Scoring Engine Delete"
    rpc_name = "scoringenginedel"
    menu_path = "scoringengine.del"
    takes_kwargs = False
    on_request_args = ['auth', 'pkid']
    def on_request(self, auth, pkid):
        return model_del(ScoringEngine, self.database_connection, pkid)

class ScoringEngineSet(CssefRPCEndpoint):
    name = "Scoring Engine Set"
    rpc_name = "scoringengineset"
    menu_path = "scoringengine.set"
    on_request_args = ['auth', 'pkid']
    def on_request(self, auth, pkid, **kwargs):
        return model_set(ScoringEngine, self.database_connection, pkid, **kwargs)

class ScoringEngineGet(CssefRPCEndpoint):
    name = "Scoring Engine Get"
    rpc_name = "scoringengineget"
    menu_path = "scoringengine.get"
    on_request_args = ['auth']
    def on_request(self, auth, **kwargs):
        return model_get(ScoringEngine, self.database_connection, **kwargs)
