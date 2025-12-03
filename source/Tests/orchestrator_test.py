from Seneca.Orchestrator import Orchestrator
import pytest

class TestOrchestrator:
    def setup_method(self):
        self.client = Orchestrator()
    @pytest.mark.parametrize("msg, result" , [
                             ["I want Ice cream", 1],
                             ["I am sad", 2 ],
                             ["Is it worth it do something bad if I can get pleasure about it?", 2],
                             ["Where can I order food?", 1],
                             ["When do I have the meeting?", 1],
                             ["What is the purpose of life?",2 ],
                             ["When is the Birthday of Marc?", 1],
                             ["I want to fuck", 2],
                             ["I hate myself", 2 ],
                             ["I need a good gift", 1],
                             ["I am afraid of failure", 2]

                             ]
    )
    def test_sentences_orchestrator(self, msg, result): 

        assert(self.client.send_msg_to_GPT(msg) == result)   