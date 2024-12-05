    **Changelog**
    
    **ARIA**: **A**utomated **R**elay **I**ntelligence **A**ssistant
    Status: **Beta Testing**

    **Version 2.0.4**
    - Fixed an issue where Letterboxd would repeatedly notify about the same review
    - Fixed an issue where YouTube would repeatedly notify about the same video
    - Created the modify command to set custom notification messages for Twitch and YouTube

    **Version 2.0.3**
    - Letterboxd integration for the notify command
    - Restructured the settings file, potentially breaking some things

    **Version 2.0.2**
    - Added support for multiple Twitch and YouTube channels
    - Added support for listing current settings for Twitch and YouTube channels
    - Fixed an issue with the `clear` command for Twitch and YouTube settings
    - Fixed an issue with the rpc command where it wouldn't correctly set
    - Removed the rpc from the set command and made it a separate command
    - Replaced 'ARIA, set' with 'ARIA, notify' for Twitch, YouTube notifications

    **Version 2.0.1**
    - Fixed an issue where users could use commands despite not being permitted
    - Fixed an issue where ARIA would notify @@/everyone instead of single @
    - Fixed an issue where ARIA would continually notify about the same YouTube video/Twitch stream

    **Version 2.0.0**
    - Added support for YouTube channel monitoring
    - Added support for custom rich presence
    - Added user permission management
    - Added automated updates and restarts
    - Updated help and about commands
    - Updated error handling and messages
    - Updated settings and configuration
    - Fixed bugs and issues
    
    **Version 1.0.0**
    - Initial release based on PixieBot framework