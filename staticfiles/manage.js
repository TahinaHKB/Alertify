var nb = 0;
        console.log (nb);
        $(document).ready(function(){
          var display = $("#display");
          setInterval(function(){ 
              $.ajax({
                  type: 'GET',
                  url : "/api/scrap/"+nb,
                  success: function(response){
                    nb = parseInt(response.nb);
                    document.getElementById("nb").innerHTML = response.nb;
                    console.log(response.nb+" / "+response.n);
                    if(response.msg=="Negative")
                        console.log("Rien à signaler");
                    else 
                        console.log("Changement");
                  },
                  error: function(response){
                      console.log('Erreur')
                  }
              });
          },5000);
      });