
const electron = require("electron");
const {app, BrowserWindow, globalShortcut} = electron; // require("electron");

const gamepadService = require("gamepad");
const network = require("net");

var dev_test = false;

process.argv.forEach(function (val, index, array) {
	if (val.toLowerCase() == "-d"){
		dev_test = true;
	}
});

process.on('uncaughtException', function (err) {
	console.log("Uncaught Exception: ", err);
}); 

//

const host = "127.0.0.1"; // RaspberryPi IP // Do ipconfig to get this once the PI server is up and running
const port = 5599;

//

var station_window;

function createWindow () {
	// Create the browser window.
	let screenSize = electron.screen.getPrimaryDisplay().workAreaSize;
	let windowOptions = {

		width : screenSize.width,
		height: 240,
		maxHeight : 240,
		minHeight : 240,

		x: 0,
		y: screenSize.height - 240,

		show: false,

		titleBarStyle: "hidden",

		webPreferences: {
			devTools: dev_test
		}

	};

	station_window = new BrowserWindow(windowOptions);

	station_window.setMenu(null);

	station_window.once("ready-to-show", () => {
		station_window.show();
		activateControlStation();
	})

	// and load the index.html of the app.
	station_window.loadFile('index.html')

	// Open the DevTools.
	station_window.webContents.openDevTools()

	// Emitted when the window is closed.
	station_window.on('closed', () => {
		// Dereference the window object, usually you would store windows
		// in an array if your app supports multi windows, this is the time
		// when you should delete the corresponding element.
		station_window = null
	})
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', createWindow)

// Quit when all windows are closed.
app.on('window-all-closed', () => {
	// On macOS it is common for applications and their menu bar
	// to stay active until the user quits explicitly with Cmd + Q
	if (process.platform !== 'darwin') {
		app.quit()
	}
})

app.on('activate', () => {
	// On macOS it's common to re-create a window in the app when the
	// dock icon is clicked and there are no other windows open.
	if (station_window === null) {
		createWindow()
	}
})

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.

/*

		HANDLER FOR RASPBERRY-RIO

*/

function activateControlStation(){

	// Initialize the library
	gamepadService.init();

	var controllerMap = {
		// USB index : { Control Station Index, deviceReference, sessionID};
	};

	// List the state of all currently attached devices
	for (var controllerIndex = 0, numberDevices = gamepadService.numDevices(); controllerIndex < numberDevices; controllerIndex++){
		console.log(controllerIndex, gamepadService.deviceAtIndex(controllerIndex));
	}

	// Create a game loop and poll for events
	setInterval(gamepadService.processEvents, 16);

	// Scan for new gamepads as a slower rate
	setInterval(gamepadService.detectDevices, 1000);

	gamepadService.on("attach", function(){
		console.log("Gamepad Connected");
		// reconnect if available mapping is found
	})

	gamepadService.on("remove", function(){
		console.log("Gamepad Disconnected");
		// clear the mappings for the disconnected gamepad
	})


	//

	const robot_server = new network.Socket();

	robot_server.connect(port, host, function(){

		console.log("Connected to: " + host + ":" + port);

		var controllerData = {};

		gamepadService.on("move", function(gamepadIndex, axis, value){

			if (Math.abs(value) < 0.02){ return; }

			console.log("Axis Moved", {
				gamepadIndex : gamepadIndex,
				axis : axis,
				value : value
			});

			controllerData[gamepadIndex] = gamepadService.deviceAtIndex(gamepadIndex);
		})

		gamepadService.on("up", function(gamepadIndex, buttonIndex){
			console.log("Button Pressed", {
				gamepadIndex : gamepadIndex,
				buttonIndex : buttonIndex
			});

			controllerData[gamepadIndex] = gamepadService.deviceAtIndex(gamepadIndex);
		})

		gamepadService.on("down", function(gamepadIndex, buttonIndex){
			console.log("Button Released", {
				gamepadIndex : gamepadIndex,
				buttonIndex : buttonIndex
			});

			controllerData[gamepadIndex] = gamepadService.deviceAtIndex(gamepadIndex);
		})

		// Sending controller poll data
		setInterval(function(){
			for (controllerIndex in controllerData){
				if ((controllerData[controllerIndex]) && ("axisStates" in controllerData[controllerIndex])){
					for (axisIndex = 0; axisIndex < controllerData[controllerIndex]["axisStates"].length; axisIndex++){
						var curAxisValue = controllerData[controllerIndex]["axisStates"][axisIndex];
						if ((curAxisValue) && (typeof curAxisValue == "number")){
							controllerData[controllerIndex]["axisStates"][axisIndex] = curAxisValue.toFixed(3)
						}
					}
				}
			}
			console.log(controllerData)
			robot_server.write(JSON.stringify({type: "ControllerData", data: controllerData}));
		}, 500); // Milliseconds


		function enable(){
			console.log("Sending ENABLE request")
			robot_server.write(JSON.stringify({type: "State", data : "Enable"}));
		}

		function disable(){
			console.log("Sending DISABLE request")
			robot_server.write(JSON.stringify({type: "State", data : "Disable"}));
		}

		enable()


	})


	function bin2String(array) {
		return String.fromCharCode.apply(String, array);
	}

	robot_server.on("data", function(data){

		console.log("Data ", bin2String(data));

	})

	robot_server.on("close", function(){
		console.log("Connection closed");
	})

	/*
			SHORTCUTS
	*/

	globalShortcut.register("Space", function(){
		console.log("EMERGENCY DISABLE");
	});

	globalShortcut.register("[+]+\\", function(){
		if (station_window.isFocused()) {
			console.log("ENABLE SHORTCUT");
		}
	});

	globalShortcut.register("Return", function(){
		if (station_window.isFocused()) {
			console.log("DISABLE SHORTCUT");
		}
	});

	// TO DO
	// Filter for disconnected controllers

	// cd C:/_PROJECTS/RaspberryRIO/ControlStation

}