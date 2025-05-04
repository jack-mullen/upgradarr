# Upgradarr

## Configuration

The configuration file should be named `config.yaml` and placed in the root directory. You can copy and modify the provided `example.config.yaml` as a starting point.

### Configuration Options

#### General Options
- `log_level`: Sets the logging level. Valid options are "debug", "info", "warning", "error". Default is "info".

#### Radarr Configuration
The `radarr` section contains settings for connecting to your Radarr instance:

- `api_key`: Your Radarr API key (required)
- `base_url`: The base URL of your Radarr instance (required)

#### Profile Configuration
The `profiles` section defines quality profile aging rules:

- Each profile should match a quality profile name in Radarr
- `active_until_days`: Number of days a movie should stay in this profile
  - Movies newer than this value will use this profile
  - Omit this for the final fallback profile
- Profiles are evaluated in order, with the first matching profile being used