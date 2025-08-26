from dotenv import load_dotenv
from fastapi import FastAPI

from vocode.logging import configure_pretty_logging
from vocode.streaming.agent.chat_gpt_agent import ChatGPTAgent
from vocode.streaming.client_backend.conversation import ConversationRouter
from vocode.streaming.models.agent import ChatGPTAgentConfig
from vocode.streaming.models.message import BaseMessage
from vocode.streaming.models.synthesizer import AzureSynthesizerConfig
from vocode.streaming.synthesizer.azure_synthesizer import AzureSynthesizer
from vocode.streaming.models.audio import AudioEncoding   # ✅ fixed import
# from vocode.streaming.models.synthesizer import CoquiTTSSynthesizerConfig
# from vocode.streaming.synthesizer.coqui_tts_synthesizer import CoquiTTSSynthesizer

load_dotenv()

app = FastAPI(docs_url=None)

configure_pretty_logging()

conversation_router = ConversationRouter(
    agent_thunk=lambda: ChatGPTAgent(
        ChatGPTAgentConfig(
            initial_message=BaseMessage(text="Hello!"),
            prompt_preamble="Have a pleasant conversation about life",
        )
    ),
    synthesizer_thunk=lambda output_audio_config: AzureSynthesizer(
        AzureSynthesizerConfig.from_output_audio_config(
            output_audio_config,
            voice_name="en-US-SteffanNeural",
        )
    ),
    # synthesizer_thunk=lambda output_audio_config: CoquiTTSSynthesizer(
    #     CoquiTTSSynthesizerConfig.from_output_audio_config(
    #         output_audio_config,
    #         tts_kwargs = {
    #             "model_name": "tts_models/en/ljspeech/tacotron2-DDC_ph"
    #         },
    #     )
    # ),
)

app.include_router(conversation_router.get_router())
