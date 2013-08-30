/* Table initialisation */
$(document).ready(function() {
	$('#book_list_table').dataTable( {
		"sDom": "<'row-fluid'<'span6'l><'span6'f>r>t<'row-fluid'<'span6'i><'span6'p>>",
		"sPaginationType": "bootstrap",
		"oLanguage": {
			"sLengthMenu": "_MENU_ records per page"
		},
		"aLengthMenu": [[-1, 100, 50, 25, 10], ["All", 100, 50, 25, 10]],
		"iDisplayLength" : -1
	} );
} );
