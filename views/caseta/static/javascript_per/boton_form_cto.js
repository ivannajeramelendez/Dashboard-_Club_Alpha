$(document).ready(function() {
    var max_fields      = 15; //maximo input 
    var wrapper   		= $(".input_fields_wrap"); //Lugar donde agregar
    var add_button      = $(".add_field_button"); //Botton Id agregar
    
    var x = 1; //Inicial text-box cuenta
    $(add_button).click(function(e){ //agregar presionando boton
      e.preventDefault();
      if(x < max_fields){ //maximo input aceptados
        x++; //incremento del text-box
        $(wrapper).append('<div><input class="form-control form-control-sm" type="text" name="mytext[]"/><a href="#" class="remove_field">Quitar</a></div>'); //add input box
      }
    });
    
    $(wrapper).on("click",".remove_field", function(e){ //click para quitar text-box
      e.preventDefault(); $(this).parent('div').remove(); x--;
    })
  });