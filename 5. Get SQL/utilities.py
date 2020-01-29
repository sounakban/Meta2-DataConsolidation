import pandas as pd


columns_data = ['gameID', 'ts', 'system_ticks', 'event_type', 'episode_number', \
                'level', 'score', 'lines_cleared', 'evt_id', 'evt_data1', \
                'evt_data2', 'curr_zoid', 'next_zoid', 'board_rep', 'zoid_rep']
columns_metadata = ["gameID", "Meta-Two build", "Exp. Start Time", "Game Start", "GameStart Tick", \
                    "CPU Tick Frequency", "SID", "USID", "ECID", "Environment", "Task", \
                    "SessionNr.", "GameNr.", "Input type", "Connected Inputs", "randSeed", \
                    "Screen resolution", "Screen dpi", "Fullscreen", "Window height", \
                    "Window width", "md5sum study", "md5sum task", "md5sum environment"]


def get_schema():
    data = pd.DataFrame(columns=columns_data)
    metaData = pd.DataFrame(columns=columns_metadata)

    data["gameID"] = pd.to_numeric(data["gameID"])
    data["episode_number"] = pd.to_numeric(data["episode_number"])
    data["level"] = pd.to_numeric(data["level"])
    data["score"] = pd.to_numeric(data["score"])
    data["lines_cleared"] = pd.to_numeric(data["lines_cleared"])
    metaData["gameID"] = pd.to_numeric(metaData["gameID"])
    metaData["SessionNr."] = pd.to_numeric(metaData["SessionNr."])
    metaData["GameNr."] = pd.to_numeric(metaData["GameNr."])
    metaData["randSeed"] = pd.to_numeric(metaData["randSeed"])
    metaData["Screen dpi"] = pd.to_numeric(metaData["Screen dpi"])
    metaData["Window height"] = pd.to_numeric(metaData["Window height"])
    metaData["Window width"] = pd.to_numeric(metaData["Window width"])

    # print(pd.io.sql.get_schema(data, "data"))
    # print(pd.io.sql.get_schema(metaData, "metaData"))

    return (data, metaData)


def get_SQLConnection():
    from sqlalchemy import create_engine
    import pymysql
    db_connection_str = 'mysql+pymysql://sounak:osboxes.org@localhost/Meta2_DB'
    con_engine = create_engine(db_connection_str)

    return con_engine


def get_dataColumns():
    return columns_data;


def get_metaDataColumns():
    return columns_metadata;