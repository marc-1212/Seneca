import pytest
import sys
import os

# Obtiene la ruta al directorio padre del directorio actual (Tests)
# Es decir, la ruta a la raíz del proyecto.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import main
class TestOrchestrator:
    @pytest.mark.parametrize("msg, result" , [
                             ["I want Ice cream", "Secretary"],
                             ["I am sad", "Seneca" ],
                             ["Is it worth it do something bad if I can get pleasure about it?", "Seneca"],
                             ["Where can I order food?", "Secretary"],
                             ["When do I have the meeting?", "Secretary"],
                             ["What is the purpose of life?","Seneca" ],
                             ["When is the Birthday of Marc?", "Secretary"],
                             ["How can I manage the anger of this moment?", "Seneca"],
                             ["I would like to have a new haircut", "Secretary" ],
                             ["I need to find a supermarket", "Secretary"],
                             ["I am afraid of failure", "Seneca"]

                             ]
    )
    def test_sentences_orchestrator(self, msg, result): 

        assert(main(msg) == result)   