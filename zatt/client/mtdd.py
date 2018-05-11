import collections
from zatt.client.abstractClient import AbstractClient
from zatt.client.refresh_policies import RefreshPolicyAlways

class MTDD(collections.UserDict, AbstractClient):
    def __init__(self, addr, port, append_retry_attempts=3,
                 refresh_policy=RefreshPolicyAlways()):
        super().__init__()
        self.data['cluster'] = [(addr, port)]
        self.append_retry_attempts = append_retry_attempts
        self.refresh_policy = refresh_policy
        self.refresh(force=True)

    def refresh(self, force=False):
        if force or self.refresh_policy.can_update():
            self.data = self._get_state()

    def send_minitransaction(self, compare_set, write_set, read_set):
        return super()._request({'type': 'enqueue', 'compare_set': compare_set,
            'write_set': write_set, 'read_set': read_set})
