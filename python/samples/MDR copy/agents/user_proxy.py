import autogen

user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="A human admin overseeing asset categorization.",
    code_execution_config={"last_n_messages": 3, "work_dir": "groupchat"},
    human_input_mode="TERMINATE"
)
