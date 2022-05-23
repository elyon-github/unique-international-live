
function get_current(){
	var now = new Date();

	var day = ("0" + now.getDate()).slice(-2);
    var month = ("0" + (now.getMonth() + 1)).slice(-2);

    var today = now.getFullYear()+"-"+(month);

    return today;
}


function construct_sawt(data){
	var html = "<table class='table table-striped table-hover'><thead><tr>";

	html += "<th scope='col'>Number</th>\
		<th scope='col'>Taxpayer Identification Number</th>\
		<th scope='col'>Corporation</th>\
		<th scope='col'>ATC Code</th>\
		<th scope='col'>Income Payment</th>\
		<th scope='col'>Tax Rate</th>\
		<th scope='col'>Tax Withheld</th></tr></thead><tbody>";

	var sub = 0;
	var tax = 0;
	var num = 1;
	for(let x in data){
		let income = Math.abs(data[x][1]);
		let rate = Math.abs(data[x][5]);
		let amount = Math.abs(data[x][0]);

		html += "<tr>";
		html += "<th scope='row'>" + num + "</td>\
			<td>" + data[x][2] + "</td>\
			<td>" + data[x][3] + "</td>\
			<td>" + data[x][4] + "</td>\
			<td>" + numberWithCommas(income) + "</td>\
			<td>" + rate + "%</td>\
			<td>" + numberWithCommas(amount) + "</td>";
		html += "</tr>"

		sub += income;
		tax += amount;
		num += 1;
	}

	html += "<tr>\
		<th scope='row'></td>\<td></td><td></td><td></td>\
		<td scope='row'>" + numberWithCommas(sub) + "</td>\
		<td></td>\
		<td scope='row'>" + numberWithCommas(tax) + "</td>\
		</tr>";

	html += "</tbody></table>";

	return html;
}

function construct_partners(data){
	var html = "";

	for(let x in data){
		html += "<option value='" + data[x][0] + "'>" + data[x][1] + "</option>";
	}

	return html;
}

function construct_slp(data){
	var html = "<table class='table table-striped table-hover'><thead><tr>";

	html += "<th scope='col'>Taxable Month</th>\
		<th scope='col'>Taxpayer Identification Number</th>\
		<th scope='col'>Registered Name</th>\
		<th scope='col'>Gross Purchase</th>\
		<th scope='col'>Exempt Purchase</th>\
		<th scope='col'>Zero-rated Purchase</th>\
		<th scope='col'>Taxable Purchase</th>\
		<th scope='col'>Purchase of Services</th>\
		<th scope='col'>Purchase of Capital goods</th>\
		<th scope='col'>Purchase of Goods other than Capital Goods</th>\
		<th scope='col'>VAT</th>\
		<th scope='col'>Gross Taxation</th>";

	var gross_sales_po_tot = 0;
	var excempt_tot = 0;
	var zero_rated_tot = 0;
	var taxable_tot = 0;
	var po_services_tot = 0;
	var po_capital_goods_tot = 0;
	var po_other_tot = 0;
	var tax_tot = 0;
	var gross_tax_tot = 0;

	var x;
	for(let y in data){
		x = JSON.parse(JSON.stringify(data[y]));

		html += "<tr>";
		html += "<th scope='row'></td>\
			<td>" + format_vat(x.vat) + "</td>\
			<td>" + numberWithCommas(x.name) + "</td>\
			<td>" + numberWithCommas(x.gross_sales_po) + "</td>\
			<td>" + numberWithCommas(x.exempt) + "</td>\
			<td>" + numberWithCommas(x.zero_rated) + "</td>\
			<td>" + numberWithCommas(x.taxable) + "</td>\
			<td>" + numberWithCommas(x.po_services) + "</td>\
			<td>" + numberWithCommas(x.po_capital_goods) + "</td>\
			<td>" + numberWithCommas(x.po_other) + "</td>\
			<td>" + numberWithCommas(x.tax) + "</td>\
			<td>" + numberWithCommas(x.gross_tax) + "</td>\
			";
		html += "</tr>"

		gross_sales_po_tot += x.gross_sales_po;
		excempt_tot += x.exempt;
		zero_rated_tot += x.zero_rated;
		taxable_tot += x.taxable;
		po_services_tot += x.po_services;
		po_capital_goods_tot += x.po_capital_goods;
		po_other_tot += x.po_other
		tax_tot += x.tax;
		gross_tax_tot += x.gross_tax;
	}

	html += "<tr><th scope='row'></td><td></td><td></td>\
		<td>" + numberWithCommas(gross_sales_po_tot) + "</td>\
		<td>" + numberWithCommas(excempt_tot) + "</td>\
		<td>" + numberWithCommas(zero_rated_tot) + "</td>\
		<td>" + numberWithCommas(taxable_tot) + "</td>\
		<td>" + numberWithCommas(po_services_tot) + "</td>\
		<td>" + numberWithCommas(po_capital_goods_tot) + "</td>\
		<td>" + numberWithCommas(po_other_tot) + "</td>\
		<td>" + numberWithCommas(tax_tot) + "</td>\
		<td>" + numberWithCommas(gross_tax_tot) + "</td></tr>";

	// html = "<p>" + JSON.stringify(data[0]) + "</p>"

	html += "</tbody></table>";

	return html;
}

function construct_sls(data){
	var html = "<table class='table table-striped table-hover'><thead><tr>";

	html += "<th scope='col'>Taxable Month</th>\
		<th scope='col'>Taxpayer Identification Number</th>\
		<th scope='col'>Registered Name</th>\
		<th scope='col'>Gross Purchase</th>\
		<th scope='col'>Exempt Purchase</th>\
		<th scope='col'>Zero-rated Purchase</th>\
		<th scope='col'>Taxable Purchase</th>\
		<th scope='col'>VAT</th>\
		<th scope='col'>Gross Taxation</th>";

	var gross_sales_po_tot = 0;
	var excempt_tot = 0;
	var zero_rated_tot = 0;
	var taxable_tot = 0;
	var tax_tot = 0;
	var gross_tax_tot = 0;
	var x;
	for(let y in data){
		x = JSON.parse(JSON.stringify(data[y]));

		html += "<tr>";
		html += "<th scope='row'></td>\
			<td>" + format_vat(x.vat) + "</td>\
			<td>" + numberWithCommas(x.name) + "</td>\
			<td>" + numberWithCommas(x.gross_sales_po) + "</td>\
			<td>" + numberWithCommas(x.exempt) + "</td>\
			<td>" + numberWithCommas(x.zero_rated) + "</td>\
			<td>" + numberWithCommas(x.taxable) + "</td>\
			<td>" + numberWithCommas(x.tax) + "</td>\
			<td>" + numberWithCommas(x.gross_tax) + "</td>\
			";
		html += "</tr>"

		gross_sales_po_tot += x.gross_sales_po;
		excempt_tot += x.exempt;
		zero_rated_tot += x.zero_rated;
		taxable_tot += x.taxable;
		tax_tot += x.tax;
		gross_tax_tot += x.gross_tax;
	}

	html += "<tr><th scope='row'></td><td></td><td></td>\
		<td>" + numberWithCommas(gross_sales_po_tot) + "</td>\
		<td>" + numberWithCommas(excempt_tot) + "</td>\
		<td>" + numberWithCommas(zero_rated_tot) + "</td>\
		<td>" + numberWithCommas(taxable_tot) + "</td>\
		<td>" + numberWithCommas(tax_tot) + "</td>\
		<td>" + numberWithCommas(gross_tax_tot) + "</td>\
		</tr>";

	// html = "<p>" + JSON.stringify(data[0]) + "</p>"

	html += "</tbody></table>";

	return html;
}

function numberWithCommas(x) {
	var str = 0;
	if (x != null) {
		str = x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
	}
    return str;
}

function format_vat(x){
	str = "None";
	if (x != null) {
		str = x.slice(0,3) + "-" + x.slice(3,6) + "-" + x.slice(6) + "-000";
	}
	return str;
}
