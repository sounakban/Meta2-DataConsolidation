import pandas as pd

columns_data = ['gameID', 'ts', 'system_ticks', 'event_type', 'episode_number', \
                'level', 'score', 'lines_cleared', 'evt_id', 'evt_data1', \
                'evt_data2', 'curr_zoid', 'next_zoid', 'board_rep', 'zoid_rep']
columns_metadata = ["gameID", "Meta-Two build", "Exp. Start Time", "Game Start", "GameStart Tick", \
            "CPU Tick Frequency", "SID", "USID", "ECID", "Environment", "Task", \
            "SessionNr.", "GameNr.", "Input type", "Connected Inputs", "randSeed", \
            "Screen resolution", "Screen dpi", "Fullscreen", "Window height", \
            "Window width", "md5sum study", "md5sum task", "md5sum environment"]

data = pd.DataFrame(columns=columns_data)
print(pd.io.sql.get_schema(data, "data"))
metaData = pd.DataFrame(columns=columns_metadata)
print(pd.io.sql.get_schema(metaData, "metaData"))
