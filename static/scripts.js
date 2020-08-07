// $(document).ready(function () {
//     $('.nav ul li:first').addClass('active');
//
//     $('.tab-content:not(:first)').hide();
//
//     $('.nav ul li a').click(function (event) {
//         event.preventDefault();
//         var content = $(this).attr('href');
//         $(this).parent().addClass('active');
//         $(this).parent().siblings().removeClass('active');
//         $(content).show();
//         $(content).siblings('.tab-content').hide();
//     });
// });

$('#wavFileUpload').on('change',function(){
                //get the file name
                var fileName = $(this).val();
                //replace the "Choose a file" label
                $(this).next('.custom-file-label').html(fileName);
            })


$('#yamlFileUpload').on('change',function(){
                //get the file name
                var fileName = $(this).val();
                //replace the "Choose a file" label
                $(this).next('.custom-file-label').html(fileName);
            })
$('#dictFileUpload').on('change',function(){
                //get the file name
                var fileName = $(this).val();
                //replace the "Choose a file" label
                $(this).next('.custom-file-label').html(fileName);
            })