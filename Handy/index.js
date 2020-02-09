function runAnimation(index, selectedActual, selectedPred, correctCount, incorrectCount){
  $.get("http://localhost:5000/predict/?index=" + index).then(
        function(response) {
            $(selectedActual).css("border", "10px solid transparent")
            $(selectedPred).css("border", "10px solid transparent")
            if(response.success === "False"){
                return
            } else {
                index++;
            }
            switch(response.actual) {
                case 1:
                    selectedActual = "#cyrindarical_act"
                    break;
                case 2:
                    selectedActual = "#tip_act"
                    break;

                case 3:
                    selectedActual = "#hook_act"
                    break;

                case 4:
                    selectedActual = "#palmar_act"
                    break;

                case 5:
                    selectedActual = "#spherical_act"
                    break;

                case 6:
                    selectedActual = "#lateral_act"
            }
            switch(response.pred) {
                case 1:
                    selectedPred = "#cyrindarical_pred"
                    break;
                case 2:
                    selectedPred = "#tip_pred"
                    break;
                case 3:
                    selectedPred = "#hook_pred"
                    break;
                case 4:
                    selectedPred = "#palmar_pred"
                    break;
                case 5:
                    selectedPred = "#spherical_pred"
                    break;
                case 6:
                    selectedPred = "#lateral_pred"
                    break;
            }

            if (response.pred === response.actual) {
                $(selectedActual).css({"border": "10px solid green"})
                $(selectedPred).css({"border": "10px solid green"})
                correctCount++
                $('#correct-count').text(correctCount);

            }
            else {
                $(selectedActual).css({"border": "10px solid red"})
                $(selectedPred).css({"border": "10px solid red"})
                incorrectCount++
               $('#incorrect-count').text(incorrectCount);

            }
            console.log(response.pred);
            console.log(response.actual);
            console.log(selectedActual);
            console.log(selectedPred);

            setTimeout(runAnimation, 250, index, selectedActual, selectedPred, correctCount, incorrectCount);
        }
    )
}

$(document).ready(function() {

    $("#predict").click(function(){
        console.log("hi");

        runAnimation(0, null,  null, 0 , 0);
    })
})