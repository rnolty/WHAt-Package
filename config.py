import os, os.path, json

from __init__ import plugins as all_plugins

def Get_config_file():
    if (not ('HOME' in os.environ)):
        return None
    home_dir = os.environ['HOME']
    config_file_dir = os.path.join(home_dir, ".config")
    if (os.path.exists(config_file_dir)):
        return os.path.join(config_file_dir, "whap.json")
    return os.path.join(home_dir, ".whap")


# called in normal runs to learn which plugins to use
def Get_chosen_plugins():
    plugins = all_plugins
    config_file_path = Get_config_file()
    if ((config_file_path is None) or (not os.path.exists(config_file_path))):
        pass                             # config file does not exist, stick with all_plugins
    else:
        try:
            with open(config_file_path) as config_file:
                config_data = json.load(config_file)
                plugins = config_data['plugins']
        except IOError:
            print("Cannot open config file", config_file_path)
        except:
            print("Invalid config file", config_file_path, "; delete it or recreate it with",
                  __file__, "-c")
    return plugins


# called in config runs to choose and permanently store choices
def Choose_plugins():
    config_file_path = Get_config_file()
    if (config_file_path is None):
        print("No place to save choices")
        exit(1)

    plugins_before = Get_chosen_plugins()        # if config file does not exist, this returns all plugins

    print ("Choose which package managers to search")
    plugins_now = {}
    for plugin_name in all_plugins.keys():
        if (plugin_name in plugins_before):
            prompt = " Yn :"
        else:
            prompt = " yN :"
        response = input(plugin_name + prompt).strip()

        if (((len(response) == 0) and (plugin_name in plugins_before)) or
            response.startswith('y') or response.startswith('Y')):
            plugins_now[plugin_name] = all_plugins[plugin_name]

    print()
    print("Saving choices", ','.join(plugins_now.keys()))

    data = {'plugins': plugins_now}
    try:
        with open(config_file_path, 'w') as config_file:
            json.dump(data, config_file)
    except IOError:
        print("Unable to open config file", config_file_path, "for writing")
        exit(1)
    except:
        print("Unable to save to config file", config_file_path)
        exit(1)

    exit(0)
