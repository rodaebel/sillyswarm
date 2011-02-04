/*
 * sillyswarm.js - Silly Swarm client-side Javascript API
 *
 * Copyright 2011 Tobias Rodaebel
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */


(function() {

  // Namespace
  var sillyswarm = sillyswarm || {};
  sillyswarm.global = this;

  var HANDSHAKE_RECEIVED = 1;

  var PLAYER_MOVED = 2;

  var PLAYER_LEFT = 3;

  /* Internal API */

  // Export symbols to the global namespace
  sillyswarm.exportSymbol = function(name, opt_object, opt_objectToExportTo) {

    var parts = name.split(".")
    var cur = opt_objectToExportTo || sillyswarm.global;

    !(parts[0] in cur) && cur.execScript && cur.execScript("var " + parts[0]);

    for(var part; parts.length && (part = parts.shift());) {
      if(!parts.length && sillyswarm.isDef(opt_object)) {
        cur[part] = opt_object
      } else {
        cur = cur[part] ? cur[part] : cur[part] = {}
      }
    }
  };

  sillyswarm.isDef = function(val) {
    return val !== undefined;
  };

  /* External API */

  // Inititalize game
  sillyswarm.init = function() {

  };

  // Make a move
  var _movePlayer = function(message, body_elem) {

    var player, x, y;

    player = document.getElementById(message.player);
    x = message.x;
    y = message.y;

    if (player == null) {

      player = document.createElement("div");
      player.setAttribute("id", message.player);
      player.setAttribute("class", "container");
      player.style.position = "absolute";

      img = document.createElement("img");
      img.setAttribute("alt", message.player);
      img.setAttribute("class", "player");
      img.setAttribute("src", "/sillyswarm/busybee.gif");
      img.setAttribute("title", message.player);

      player.appendChild(img);

      body_elem.appendChild(player);
    }

    if (x < 0 || y < 0) {
      player.style.display = "none";
      player = null;
    }
    else {
      $("#"+message.player).animate({left: x-50+"px", top: y-50+"px"}, 500);
    }
    
  };

  // Remove player
  var _removePlayer = function(message, body_elem) {

    var player;

    player = document.getElementById(message.player);

    if (player == null) return;

    body_elem.removeChild(player);

  };


  /* Exporting the public API */
  sillyswarm.exportSymbol("sillyswarm.HANDSHAKE_RECEIVED", HANDSHAKE_RECEIVED);
  sillyswarm.exportSymbol("sillyswarm.PLAYER_MOVED", PLAYER_MOVED);
  sillyswarm.exportSymbol("sillyswarm.PLAYER_LEFT", PLAYER_LEFT);
  sillyswarm.exportSymbol("sillyswarm.init", sillyswarm.init);
  sillyswarm.exportSymbol("sillyswarm.movePlayer", _movePlayer);
  sillyswarm.exportSymbol("sillyswarm.removePlayer", _removePlayer);

})();
