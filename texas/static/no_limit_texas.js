<script type="text/javascript">
  $(document).ready(function(){
    console.log("ready");
    // update gui
    update();
    // add button click listener
    $("#next").click(function(){do_action("next")});
    $("#fold").click(function(){do_action("fold")});
    $("#check").click(function(){do_action("check")});
    $("#call").click(function(){do_action("call")});
    $("#min_bet").click(function(){do_action("min_bet")});
    $("#half_pot").click(function(){do_action("half_pot")});
    $("#one_pot").click(function(){do_action("one_pot")});
    $("#all_in").click(function(){do_action("all_in")});
    $("#bet_to").click(function(){do_action("bet_to")});

    function update(){
      console.log("update")
      $.get("{% url 'texas:action' %}",{"action":"update"}, do_update);
    };

    function do_update(ret){
      console.log("do update");
      // console.log(ret)

      do_update_cards(ret);
      do_update_chips(ret);
      do_update_information(ret);
      do_update_buttons(ret);

      try_invoke_update(ret);
    };

    function do_update_cards(ret){
      // update player_hole
      if(ret.hole != null){
        for (var i = 0; i < ret.hole.length; i++) {
          card_str = ret.hole[i];
          rank = card_str.slice(0,1);
          suit = card_str.slice(1,2);
          card_rank_id = "#player_card_" + i + "_rank";
          card_suit_id = "#player_card_" + i + "_suit";
          $(card_rank_id).html(rank);
          $(card_suit_id).html(str_to_suit(suit));
        }
      }
      if(ret.public_cards != null){
        for (var i = 0; i < ret.public_cards.length; i++) {
          card_str = ret.public_cards[i];
          rank = card_str.slice(0,1);
          suit = card_str.slice(1,2);
          card_rank_id = "#public_card_" + i + "_rank";
          card_suit_id = "#public_card_" + i + "_suit";
          $(card_rank_id).html(rank);
          $(card_suit_id).html(str_to_suit(suit));
        }
      }
      if(ret.opponent_hole != null){
        for (var i = 0; i < ret.opponent_hole.length; i++) {
          card_str = ret.opponent_hole[i];
          rank = card_str.slice(0,1);
          suit = card_str.slice(1,2);
          card_rank_id = "#opponent_card_" + i + "_rank";
          card_suit_id = "#opponent_card_" + i + "_suit";
          $(card_rank_id).html(rank);
          $(card_suit_id).html(str_to_suit(suit));
        }
      }

    }; // function do_update_cards end

    function do_update_chips(ret){
      console.log("---to update chips");
      var player_spent = ret.spent;
      var opponent_spent = ret.opponent_spent;
      var player_stack = 20000 - player_spent;
      var opponent_stack = 20000 - opponent_spent;
      $("#opponent_stack").html(opponent_stack);
      $("#opponent_bet").html(opponent_spent);
      $("#player_stack").html(player_stack);
      $("#player_bet").html(player_spent);
    }

    function do_update_buttons(ret){
      var next_hand_flag = false;
      var fold_flag = false;
      var check_flag = false;
      var call_flag = false;
      var min_bet_flag = false;
      var half_pot_flag = false;
      var one_pot_flag = false;
      var all_in_flag = false;
      var bet_to_falg = false;
      for(index in ret.actions){
        action = ret.actions[index];
        if(action == "next"){
          next_hand_flag = true;
        } else if(action == "fold"){
          fold_flag = true;
        } else if (action == "check") {
          check_flag = true;
        } else if (action == "call") {
          call_flag = true;
        } else if (action == "min_bet") {
          min_bet_flag = true;
        } else if (action == "half_pot") {
          half_pot_flag = true;
        } else if (action == "one_pot") {
          one_pot_flag = true;
        } else if (action == "all_in") {
          all_in_flag = true;
        } else if (action == "bet_to") {
          bet_to_falg = true;
        }

        if(next_hand_flag) {
          $("#next").attr("disabled", false); 
        } else {
          $("#next").attr("disabled", true); 
        }
        if(fold_flag){
          $("#fold").attr("disabled", false); 
        } else {
          $("#fold").attr("disabled", true); 
        }
        if(check_flag) {
          $("#check").attr("disabled", false); 
        } else {
          $("#check").attr("disabled", true); 
        }
        if(call_flag) {
          $("#call").attr("disabled", false); 
        } else {
          $("#call").attr("disabled", true); 
        }
        if(min_bet_flag) {
          $("#min_bet").attr("disabled", false); 
        } else {
          $("#min_bet").attr("disabled", true); 
        }
        if(half_pot_flag) {
          $("#half_pot").attr("disabled", false); 
        } else {
          $("#half_pot").attr("disabled", true); 
        }
        if(one_pot_flag) {
          $("#one_pot").attr("disabled", false); 
        } else {
          $("#one_pot").attr("disabled", true); 
        }
        if(all_in_flag) {
          $("#all_in").attr("disabled", false); 
        } else {
          $("#all_in").attr("disabled", true); 
        }
        if(bet_to_falg) {
          $("#bet_to").attr("disabled", false); 
        } else {
          $("#bet_to").attr("disabled", true); 
        }
      }
    };

    // update message, history, socre
    function do_update_information(ret){
      $("#message").html(ret.message);
      $("#score").html(ret.score);
    };

    function do_action(action){
      // construct action
      var context;
      if(action == "next"){
        console.log("reset...");
  reset_gui();
        context = {"action": "next", "amount" : "null"};
      } else if (action == "fold"){
        context = {"action": "fold", "amount": null};
      } else if(action == "check"){
        context = {"action": "check", "amount": null};
      } else if (action == "call"){
        context = {"action": "call", "amount": null};
      } else if (action == "min_bet"){
        context = {"action": "min_bet", "amount": null}
      } else if (action == "half_pot"){
        context = {"action": "half_pot", "amount": null}
      } else if (action == "one_pot"){
        context = {"action": "one_pot", "amount": null}
      } else if (action == "all_in"){
        context = {"action": "all_in", "amount": null}
      } else if (action == "bet_to"){
        console.log("bet_to");
        var amount = $("#amount").val();
        console.log(amount);
        context = {"action": "bet_to", "amount": amount};
      }
      // send action
      $.get("{% url 'texas:action' %}", context, do_update); 
    };

    function try_invoke_update(ret){
      if(ret.player_turn == false){
        if(ret.gameover == true){
          console.log("gameover");
          reset_gui();
        } else{
          update();
        }
      }
    };

    function reset_gui(){
      $("#message").html("");
     
      $("#opponent_card_0_rank").html("");
      $("#opponent_card_0_suit").html("");
      $("#opponent_card_1_rank").html("");
      $("#opponent_card_1_suit").html("");
      $("#public_card_0_rank").html("");
      $("#public_card_0_suit").html("");
      $("#public_card_1_rank").html("");
      $("#public_card_1_suit").html("");
      $("#public_card_2_rank").html("");
      $("#public_card_2_suit").html("");
      $("#public_card_3_rank").html("");
      $("#public_card_3_suit").html("");
      $("#public_card_4_rank").html("");
      $("#public_card_4_suit").html("");
      $("#player_card_0_rank").html("");
      $("#player_card_0_suit").html("");
      $("#player_card_1_rank").html("");
      $("#player_card_1_suit").html("");
    };





    function str_to_suit(suit){
      if(suit == 'h'){
        return '♥';
      } else if(suit == 'c'){
        return '♣';
      } else if(suit == 's'){
        return '♠';
      }else{
        return '♦';
      }
    };

  })
</script>