from ..._module_types import ModelName

class Actions_Interface():

    def register_action(
        self,
        model_name: ModelName,
        action_name: str,
        action_callback,
    ) -> None:
        ...

    def run_action(
        self,
        user_id: int,
        model_name: ModelName,
        action_name: str,
        record_id: int,
    ) -> None:
        ...

    def register_model(
        self,
        model_name: ModelName,
    ) -> None:
        ...

    def unregister_model(
        self,
        model_name: ModelName,
    ) -> None:
        ...
