var users = {};

function updateFilters()
{	
	var list = $("#playlist-select");	
	reqTitle = $("#filter-title").val().toLowerCase()
	
	// Hide by title
	list.children().each(function()
	{
		var item = $(this);
		var title = item.text().toLowerCase();
		var inactive = item.attr("disabled") == "disabled";
		var displayInactive = $("#show-removed-songs").prop("checked");

		if((inactive && !displayInactive) || title.search(reqTitle) == -1)
			item.hide();
		else
			item.show();
	});
}

function timer()
{
	$.get(
		"/api/time", function(data) {
			$('#songtext').text(data);
			$('#song-progress').val(data);
		}
	);
	
	$.get(
		"/api/length", function(data) {
			$('#song-progress').attr("max", data);
		}
	);
	
	$.get(
		"/api/volume", function(data) {
			$('#song-volume').val(data);
		}
	);
}

function timerz()
{
	if(isPlaying)
	{
		time = parseInt($('#time').val()) + 1;
		
		$('#time').val(time);
		updateTime(time, null);
	}
}

function updateTime(time, length)
{
	if(length < 0)
	{
		$("#time-pos-text").text("...");
		$("#time-length-text").text("...");
		
		return;
	}
	
	posMinutes = Math.floor(time / 60);
	if(time % 60 < 10)
		posSeconds = "0" + time % 60;
	else
		posSeconds = time % 60;
	$("#time-pos-text").text(posMinutes + ":" + posSeconds);
	
	if(length != null) {
		lenMinutes = Math.floor(length / 60);
		if(length % 60 < 10)
			lenSeconds = "0" + length % 60;
		else
			lenSeconds = length % 60;
		$("#time-length-text").text(lenMinutes + ":" + lenSeconds);
	}
}

var isPlaying = false;
function updateStatus()
{
	$.getJSON(
		"/api/status", function(data, status, xhr) {
			$("#title").text(data.title);
			$("#time").attr('max', data.length);
			$("#time").val(data.time);
			
			$("#volume").val(data.volume);
			
			if(data.volume < 0)
				$("#volume-text").text("...");
			else
				$("#volume-text").text(data.volume + "%")
			
			isPlaying = data.playing;
			$("#button-start").attr("disabled", isPlaying);
			$("#button-stop").attr("disabled", !isPlaying);
			
			updateTime(data.time, data.length);
		}
	);
	
	$.getJSON(
		"/api/queue", function(data, status, xhr) {
			$("#queue-select").empty();
			
			var i;
			for(i = 0; i < data.length; i++)
			{
				var id = data[i].pk;
				var item = data[i].fields;
				var title = item.title;
				
				$("#queue-select").append(`<option value="${id}">${title}</option>`);
			}
		}
	);
}

var recentLog = -1
function waitStatusChange()
{
	$.get(`/api/logger/wait/${recentLog}`, function(data) {
		
		$.getJSON(`/api/logger/${recentLog}`, function(data, status, xhr) {
			for(var a = 0; a < data.length; a++) {
				var text = data[a];
				$("#log").append(`<div class="log-message"><pre>${text}</pre></div>`)
			}
			
			var scrollHeight = document.getElementById("log").scrollHeight;
			$("#log").scrollTop(scrollHeight);
			
			var scrollHeight = document.getElementById("player-panels-right").scrollHeight;
			$("#player-panels-right").scrollTop(scrollHeight);
		});
		
		recentLog = data;
		updateStatus();
		waitStatusChange();
	});
}

function addToQueueField(o)
{
	//alert($(this));
	//alert(Object.keys($(this)));
	//alert(Object.keys(o));
	//alert(o.context.text);
	//alert(o.context.value);
	
	var ids = $("#queue").val()
	if(ids.length > 0)
		ids = ids + " "
	ids = ids + o.context.value;
	
	$("#queue").val(ids)
	
	//alert(Object.keys(o.context));
}

function displaySongInfo(o)
{
	userId = o.attr("userId");
	displayName = users[userId];
	
	//alert(userId);
	
	$("#songIndex").val(o.val());
	$("#username").val(displayName);
	$("#skipCounter").val(o.attr("skipCounter"));
	$("#queueCounter").val(o.attr("queueCounter"));
}

function submitQueueField()
{
	var ids = $("#queue").val()
	
	if(ids.length == 0)
	{
		alert("Add something to queue...");
		return;
	}
	
	$.get(`/api/queue/${ids}`);
	$("#queue").val("")
}

var playlist;

$(document).ready(function () {
	$.getJSON(
		"/api/users", function(data, status, xhr) {
			var i;
			for(i = 0; i < data.length; i++)
			{
				var id = data[i].pk;
				var item = data[i].fields;
				var displayName = item.displayName;
				users[id] = displayName;
			}
		}
	);
	
	$.getJSON(
		"/api/playlist/all", function(data, status, xhr) {
			playlist = data;
			var i;
			for(i = 0; i < data.length; i++)
			{
				var id = data[i].pk;
				var item = data[i].fields;
				var title = item.title;
				var active = item.active;
				//var displayInactive = $("#show-removed-songs").checked;
				//if(active || displayInactive)
				//{
					var activeTag = (!active) ? "disabled=\"disabled\"" : "";
					$("#playlist-select").append(`<option ${activeTag} value="${id}" userId="${item.user}" skipCounter="${item.skipCounter}" queueCounter="${item.queueCounter}" onclick="displaySongInfo($(this))" ondblclick="addToQueueField($(this))" >${title}</option>`);
				//}
			}
			
			updateFilters();
		}
	);
	
	$("#playlist-select").change(function(o) {
		var child = $(o.target).children()[o.target.value];
		displaySongInfo($(child));
	});
	
	updateStatus();
	waitStatusChange();
});

setInterval(timerz, 1000);
//setInterval(timer, 10000);