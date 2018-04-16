var selectList = [
	['Brand Name', 'brand_name', "Product's Marketing Name"],
	['Company Name', 'company_name', ''],
	['Device Class', 'device_class', '1, 2, or 3'],
	['Device Description', 'device_description', ''],
	['Device Name', 'device_name', ''],
	['ID', 'identifiers.id', '14 digit # starting with "00"'],
	['Medical Specialty Description', 'medical_specialty_description', 'e.g. Orthopedic, Opthalmic'],
	['Regulation Number', 'regulation_number', 'e.g. 888.3070, 868.5260'],
	['Version or Model Number', 'version_or_model_number', '']
];
jQuery(document).ready(function() {
	currentPage = 0;
	currentTotal = 0;
	baseUrl = '';
	results = [];
	jQuery('#queryAPI').on('submit', function(e) {
		e.preventDefault();
		var jQueryinputs = jQuery('#queryAPI :input');
		var params = {};
		jQueryinputs.each(function() {
			if (this.name !== '') {
				params[this.name] = jQuery(this).val();
			}
		});
		var outputParams = buildParams(params);
		console.log(outputParams);
		checkAPI(outputParams);
		storeParams(outputParams);
	});
	jQuery(document).keypress(function(e) {
		if (e.which == '13') {
			e.preventDefault();
			jQuery('#queryAPI').submit();
		}
	});
	var prevSearchTerms = [];
	Object.keys(sessionStorage).forEach(function(key) {
		if (key.search(/^search-/) !== -1) {
			prevSearchTerms.push([key.slice(7), sessionStorage.getItem(key)]);
		}
	});
	if (prevSearchTerms.length > 0) {
		prevSearchTerms.forEach(function(term) {
			var formDiv = addFormField(term[1], term[0]);
		});
		jQuery('#queryAPI').submit();
	} else {
		addFormField();
	}
});
function storeParams(params) {
	Object.keys(sessionStorage).forEach(function(sessionKey) {
		if (sessionKey.search(/^search-/) !== -1) {
			sessionStorage.removeItem(sessionKey);
		}
	});
	Object.keys(params.search).forEach(function(key) {
		sessionStorage.setItem('search-' + key, params.search[key]);
	});
}
function addDropDown(type) {
	var dropDown = jQuery(document.createElement('select'));
	selectList.forEach(function(value) {
		var option = jQuery(document.createElement('option'));
		option.html(value[0]);
		option.val(value[1]);
		if (value[1] === type) {
			option.attr('selected', true);
		}
		dropDown.append(option);
	});
	dropDown.attr('onchange', 'setName(this)');
	return dropDown;
}
function setName(obj) {
	var value = jQuery(obj).val();
	var input = jQuery(obj).prev();
	input.attr('name', value);
	selectList.forEach(function(options) {
		if (options[1] == value) {
			input.attr('placeholder', options[2]);
		}
	});
}
function addFormField(inputVal, type) {
	var queryDiv = jQuery(document.createElement('div'));
	queryDiv.addClass('searchfield');

	var queryInput = jQuery(document.createElement('input'));
	queryInput.attr('type', 'text');
	queryInput.addClass('biginput');
	if (inputVal) {
		queryInput.attr('name', type);
		selectList.forEach(function(selection) {
			if (selection[1] === type) {
				queryInput.attr('placeholder', selection[0]);
			}
		});
		queryInput.val(inputVal);
	} else {
		queryInput.attr('autofocus', 'autofocus');
		queryInput.attr('name', 'company_name');
		queryInput.attr('placeholder', 'Company Name');
	}
	if (type) {
		var dropDown = addDropDown(type);
	} else {
		var dropDown = addDropDown('company_name');
	}
	var closeButton = jQuery(document.createElement('button'));
	closeButton.addClass('close-button');
	closeButton.attr('onclick', 'removeFormField(this)');
	closeButton.html('X');

	queryDiv.append(queryInput, dropDown, closeButton);
	jQuery('#form-submit').before(queryDiv);
	queryInput.click();
	checkSearchCount();
}
function checkSearchCount() {
	var searchTerms = jQuery('.searchfield');
	if (searchTerms.length > 1) {
		jQuery('.close-button').css('display', 'inline');
	} else {
		jQuery('.close-button').css('display', 'none');
	}
}
function removeFormField(obj) {
	jQuery(obj)
		.parent()
		.remove();
	checkSearchCount();
}
function buildParams(params) {
	var output = {
		search: {},
		limit: 10,
		skip: 0
	};
	Object.keys(params).forEach(function(key) {
		output.search[key] = params[key];
	});
	return output;
}
function storeValue(index) {
	Object.keys(results[index]).forEach(function(key) {
		switch (key) {
			case 'sterilization':
				var array = results[index][key];
				Object.keys(array).forEach(function(keyValues) {
					sessionStorage.setItem(keyValues, array[keyValues]);
					console.log([keyValues, array[keyValues]]);
				});
				break;
			case 'identifiers':
				var array = results[index][key];
				array.forEach(function(subObject, index) {
					Object.keys(subObject).forEach(function(subKey) {
						sessionStorage.setItem(`identifiers-jQuery{index}-jQuery{subKey}`, subObject[subKey]);
						console.log([`identifiers-jQuery{index}-jQuery{subKey}`, subObject[subKey]]);
					});
				});
				break;
			case 'product_codes':
				var array = results[index][key];
				array.forEach(function(subObject, index) {
					Object.keys(subObject).forEach(function(subKey) {
						if (typeof subObject[subKey] == 'object') {
							var openfda = subObject[subKey];
							Object.keys(openfda).forEach(function(openfdaKey) {
								sessionStorage.setItem(`openfda-jQuery{index}-jQuery{openfdaKey}`, openfda[openfdaKey]);
								console.log([`openfda-jQuery{index}-jQuery{openfdaKey}`, openfda[openfdaKey]]);
							});
						} else {
							sessionStorage.setItem(`product_codes-jQuery{index}-jQuery{subKey}`, subObject[subKey]);
							console.log([`product_codes-jQuery{index}-jQuery{subKey}`, subObject[subKey]]);
						}
					});
				});
				break;
			case 'customer_contacts':
				var array = results[index][key][0];
				Object.keys(array).forEach(function(subKey) {
					sessionStorage.setItem(`customer_contacts-jQuery{subKey}`, array[subKey]);
					console.log([`customer_contacts-jQuery{subKey}`, array[subKey]]);
				});
				break;
			case 'gmdn_terms':
				var array = results[index][key][0];
				Object.keys(array).forEach(function(subKey) {
					sessionStorage.setItem(`gmdn_terms-jQuery{subKey}`, array[subKey]);
					console.log([`gmdn_terms-jQuery{subKey}`, array[subKey]]);
				});
				break;
			default:
				sessionStorage.setItem(key, results[index][key]);
				console.log([key, results[index][key]]);
		}
	});
	window.location.assign('Recall.html');
}
function checkAPI(params, url) {
	// console.log(url);
	if (!url) {
		var url = `https://api.fda.gov/device/udi.json?`;
		paramOutput = [];
		Object.keys(params).forEach(function(key) {
			if (key == 'search') {
				url += 'search=';
				Object.keys(params[key]).forEach(function(value) {
					if (params[key][value] !== '') {
						paramOutput.push(`jQuery{value}:"jQuery{params[key][value]}"`);
					}
				});
				if (paramOutput.length > 1) {
					url += paramOutput.join('+AND+');
				} else if (paramOutput.length === 1) {
					url += paramOutput[0];
				}
				baseUrl = url;
			} else if (key == 'skip') {
				if (params[key] !== 0) {
					url += `&jQuery{key}=jQuery{params[key]}`;
				}
			}
		});
	} else {
		url += `&skip=jQuery{params.skip}`;
	}
	console.log(url);
	jQuery
		.ajax({
			url: url + '&limit=10'
		})
		.done(function(result) {
			// console.log(result.meta.results);
			currentPage = result.meta.results.skip;
			jQuery('#outputbox').html(dataDisplayBuilder(result, baseUrl));
		})
		.fail(function(error) {
			jQuery('#outputbox').html(error.responseJSON.error.message);
		});
}
function dataDisplayBuilder(result, url) {
	skipCount = currentPage;
	totalCount = result.meta.results.total;
	var containerDiv = jQuery(document.createElement('div'));
	var forwardButton = jQuery(document.createElement('button'));
	forwardButton.html('▶');
	forwardButton.attr('onclick', `checkAPI({search:{},skip:jQuery{skipCount + 10}},'jQuery{url}')`);
	if (totalCount - skipCount < 10) {
		forwardButton.attr('disabled', 'disabled');
	} else {
		forwardButton.removeAttr('disabled');
	}
	var backButton = jQuery(document.createElement('button'));
	backButton.html('◀');
	backButton.attr('onclick', `checkAPI({search:{},skip:jQuery{skipCount - 10}},'jQuery{url}')`);
	backButton.css('margin', '5px');
	if (skipCount >= 10) {
		backButton.removeAttr('disabled');
	} else {
		backButton.attr('disabled', 'disabled');
	}
	var counter = jQuery(document.createElement('p'));
	if (totalCount - skipCount < 10) {
		counter.html(`Showing jQuery{skipCount + 1} - jQuery{totalCount} of jQuery{totalCount}`);
	} else {
		counter.html(`Showing jQuery{skipCount + 1} - jQuery{skipCount + 10} of jQuery{totalCount}`);
	}
	var data = result.results;
	window.results = data;
	var list = jQuery(document.createElement('ul'));
	list.addClass('api-results');
	data.forEach(function(obj, index) {
		var item = jQuery(document.createElement('li'));
		var title = jQuery(document.createElement('div'));
		title.addClass('title');
		var description = jQuery(document.createElement('div'));
		description.addClass('description');
		var companyLine = jQuery(document.createElement('div'));
		companyLine.addClass('company-line');
		item.append(title, description, companyLine);
		Object.keys(obj).forEach(function(key) {
			switch (key) {
				case 'brand_name':
					var a = jQuery(document.createElement('a'));
					a.addClass('title');
					a.attr('href', `#`);
					a.attr('onclick', `storeValue(jQuery{index})`);
					a.html(`jQuery{obj[key]} - jQuery{obj.identifiers[0].id}`);
					title.append(a);
					break;
				case 'device_description':
					description.append(`<p>jQuery{obj[key]}</p>`);
					break;
				case 'company_name':
					companyLine.append(
						`<div><span class="redTitle">Company Name: </span><span>jQuery{obj[key]}</span></div>`
					);
					break;
				case 'version_or_model_number':
					companyLine.append(
						`<div><span class="redTitle">Version or Model: </span><span>jQuery{obj[key]}</span></div>`
					);
					break;
			}
		});
		list.append(item);
	});
	var headerDiv = jQuery(document.createElement('div'));
	headerDiv.addClass('header');
	headerDiv.append(counter, backButton, forwardButton);
	containerDiv.append(headerDiv, list);
	containerDiv.addClass('output-container');
	return containerDiv;
}
function dataSorter(data, searchTerms) {
	var output = [];
	data.results.forEach(function(result) {
		var deviceClass = result.openfda.device_class;
		var matched = false;
		searchTerms.deviceClass.forEach(function(dClass) {
			if (dClass == deviceClass) {
				matched = true;
			}
		});
		var regulationNumber = result.openfda.regulation_number;
		if (matched) {
			searchTerms.regulationNumber.forEach(function(number) {
				if (regulationNumber == number) {
					output.push(result);
				}
			});
		}
	});
	return output;
}
