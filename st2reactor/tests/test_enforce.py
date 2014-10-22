import datetime

import mock
import unittest2

from st2common.models.db.reactor import TriggerDB, TriggerInstanceDB, \
    RuleDB, ActionExecutionSpecDB
from st2common.models.db.action import ActionDB, ActionExecutionDB
import st2common.services.action as action_service
from st2common.util import reference
from st2reactor.rules.enforcer import RuleEnforcer
import st2tests.config as tests_config

MOCK_TRIGGER = TriggerDB()
MOCK_TRIGGER.id = 'trigger-test.id'
MOCK_TRIGGER.name = 'trigger-test.name'
MOCK_TRIGGER.content_pack = 'dummypack1'

MOCK_TRIGGER_INSTANCE = TriggerInstanceDB()
MOCK_TRIGGER_INSTANCE.id = 'triggerinstance-test'
MOCK_TRIGGER_INSTANCE.trigger = reference.get_ref_from_model(MOCK_TRIGGER)
MOCK_TRIGGER_INSTANCE.payload = {}
MOCK_TRIGGER_INSTANCE.occurrence_time = datetime.datetime.utcnow()

MOCK_ACTION = ActionDB()
MOCK_ACTION.id = 'action-test-1.id'
MOCK_ACTION.name = 'action-test-1.name'

MOCK_ACTION_EXECUTION = ActionExecutionDB()
MOCK_ACTION_EXECUTION.id = 'actionexec-test-1.id'
MOCK_ACTION_EXECUTION.name = 'actionexec-test-1.name'
MOCK_ACTION_EXECUTION.status = 'scheduled'

MOCK_RULE_1 = RuleDB()
MOCK_RULE_1.id = 'rule-test-1'
MOCK_RULE_1.trigger = reference.get_str_resource_ref_from_model(MOCK_TRIGGER)
MOCK_RULE_1.criteria = {}
MOCK_RULE_1.action = ActionExecutionSpecDB()
MOCK_RULE_1.action.action = reference.get_ref_from_model(MOCK_ACTION)
MOCK_RULE_1.enabled = True

MOCK_RULE_2 = RuleDB()
MOCK_RULE_2.id = 'rule-test-2'
MOCK_RULE_2.trigger = reference.get_str_resource_ref_from_model(MOCK_TRIGGER)
MOCK_RULE_2.criteria = {}
MOCK_RULE_2.action = ActionExecutionSpecDB()
MOCK_RULE_2.action.action = reference.get_ref_from_model(MOCK_ACTION)
MOCK_RULE_2.enabled = True


class EnforceTest(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        tests_config.parse_args()

    @mock.patch.object(action_service, 'schedule', mock.MagicMock(
        return_value=MOCK_ACTION_EXECUTION))
    def test_ruleenforcement_occurs(self):
        enforcer = RuleEnforcer(MOCK_TRIGGER_INSTANCE, MOCK_RULE_1)
        execution_id = enforcer.enforce()
        self.assertTrue(execution_id is not None)
