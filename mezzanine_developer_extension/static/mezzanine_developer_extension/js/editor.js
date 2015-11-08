
var developer_editor = {
	texteditor_text_preview: undefined,
	texteditor_text_format: undefined,
	addImageToEditor: function(src){
		if (src != null){
			var $texteditor = $("#wmd-input");
			var cursorPos = $texteditor.prop('selectionStart');
			var img_html = "<img src='"+ src +"' alt='[Specify]' class='blogpostImg sampleimg'/>\r\n"+
			"<div class='imgfooter'>You can pick a picture using a filebrowser when installing mezzanine_developer_extension.</div>"
			;
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
		// We include the csrftoken for ajax django calls. 
		var html = $("#wmd-input").val();
		if (html == developer_editor.texteditor_text_preview){
			// Not doing any action if the text has not change.
			// Avoiding extra ajax calls.
			return;
		}
		developer_editor.texteditor_text_preview = html;
		
		$.post(
			"/blog/mezzanine_developer_extension/get_preview/",
			{ 'data': html,
			  'csrfmiddlewaretoken':  document.getElementsByName("csrfmiddlewaretoken")[0].value }
		).done(function(data){
			var html_data = data.html_code_preview;
			$("#previewContainer").html(html_data);
		}).fail(function(data){
			console.log(data);
		});
	},
	check_format_post: function(){
		/* Checks the format of the post via Ajax.
		*/
		var html = $("#wmd-input").val();
		if (html == developer_editor.texteditor_text_format){
			// Not doing any action if the text has not change.
			// Avoiding extra ajax calls.
			return;
		}
		developer_editor.texteditor_text_format = html;
		$("#formatinfo").html("Checking format...");
		$("#formatinfo").removeClass("formatKO");
		$("#formatinfo").removeClass("formatOK");
		$("#formatinfo").attr("title", "");
		$.post(
			"/blog/mezzanine_developer_extension/check_format/",
			{ 'data': html ,
		 	  'csrfmiddlewaretoken':  document.getElementsByName("csrfmiddlewaretoken")[0].value}
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