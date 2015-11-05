
var developer_editor = {
	addImageToEditor: function(src){
		if (src != null){
			var $texteditor = $("#wmd-input");
			var cursorPos = $texteditor.prop('selectionStart');
			var img_html = "<img src='"+ src +"' alt='[Specify]' class='blogpostImg'/>";
			developer_editor.addTextToEditor($texteditor, img_html, cursorPos);
		}
	},
	addTextToEditor: function($textarea, text, position){
		/* Adds text to $textarea.
		Text added at the cursor position specified by the parameter.
		When position is null, text is added at the end of the textarea
		*/
	    var v = $textarea.val();
	    var textBefore = v.substring(0, position);
	    var textAfter  = v.substring(position,v.length);
	    var new_val = textBefore + text + textAfter;
	    $textarea.val(new_val);
	},
	preview_post: function(){
		/*Previewing post in div.*/
		// We do not need to add csrftoken as mezzanine admin automatically
		// performs all ajax queries including it.
		var html = $("#wmd-input").val();
		$.post(
			"/blog/mezzanine_developer_extension/get_preview/",
			{ 'data': html }
		).done(function(data){
			var html_data = data.html_code_preview;
			$("#previewContainer").html(html_data);
		});
	},
	check_format_post: function(){
		/* Checks the format of the post via Ajax.
		*/
		var html = $("#wmd-input").val();
		$("#formatinfo").html("Checking format...");
		$("#formatinfo").removeClass("formatKO");
		$("#formatinfo").removeClass("formatOK");
		$("#formatinfo").attr("title", "");
		$.post(
			"/blog/mezzanine_developer_extension/check_format/",
			{ 'data': html }
		).done(function(data){
			var is_valid = data.format_code;
			var error_message = data.error_message;
			if (is_valid){
				$("#formatinfo").addClass("formatOK");
				$("#formatinfo").html("Format is valid");
			}
			else{
				$("#formatinfo").addClass("formatKO");
				$("#formatinfo").html("Invalid format");
				$("#formatinfo").attr("title", error_message);
			}
		});
	}
}