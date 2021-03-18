# mcsimplequery
Just a simple Minecraft Server query website application using Python, some JavaScript, and a little bit of simple HTML. This project is intended for people who want to host a website to specifically display the current status of a Minecraft Server.

## How to install?
### Prerequisites and dependencies
1. Apache or any other HTML webserver
2. Access to the webserver's CLI either through SSH or any other means
3. Python 3.8 or above
4. Dependency: Dinnerbone's [mcstatus](https://github.com/dinnerbone/mcstatus)
5. Dependency: Daniel Bader's [Schedule](https://github.com/dbader/schedule)
6. A Minecraft server to query

### Installation process
1. Install Python 3.8 or above.
2. Install dependencies. Do `pip install mcstatus` and `pip install schedule`.
3. Clone this repository. Do `git clone https://github.com/alzhahir/mcsimplequery`.
4. Move `status.html` to the webserver HTML website directory. For example, `/var/www/html/` for most Apache webservers.
5. You can either rename and move `config.json.example` to the same folder as `main.py` or you can also just let `main.py` to create a new `config.json` file for you.
6. Change the `config.json` to what you need.
7. Create a new Screen or tmux instance and launch `main.py`.
8. Restart the webserver.

## Configuration options
### `domainAddress`
`domainAddress` is the value of the IPv4 or domain name of the Minecraft Server you want to query.

### `serverPort`
`serverPort` is the server's port value.

### `rateRefresh`
`rateRefresh` is the frequency of which the application will requery the Minecraft Server. Value in minutes.

### `outputDir`
  `outputDir` specifies where the output file `serverstatus.js` should be placed, which is used by `status.html`. Please make sure that the directory is the same as the one in `status.html` or the app will not work.

## Contact
You can contact me through my [e-mail](mailto:megatalzhahirdaniel@gmail.com), [website](https://www.alzhahir.com/contact) or through [Discord](https://discord.gg/wm6V3cT).

**Thank you for using this project! If you like this project, be sure to star it!**
