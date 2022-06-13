import os
import xlsxwriter
from datetime import date
import processHostUnits as hu
from datetime import datetime, date, timedelta
import config_properties as prop

os.environ['prod-domain'] = 'aef22891'
os.environ[
    'prod-api-token'] = 'dt0c01.XHFZBYH6P3WU7MEXWXTJUKLZ.PBHHVPHLNA7P4SGUOWF3D6DXX3HGKWJZY2UHUZFJ4QSYZITQ5CUSGXUD4YLCFOOE'

# Tenant Information
TenantURL = "https://" + os.environ.get('prod-domain') + ".live.dynatrace.com/"
Token = os.environ.get('prod-api-token')


def createexcel(tenantURL, token, envtype, workbook):
    outlist = {}

    HUBreakdown = workbook.add_worksheet(envtype + " Hostunits")

    TitleFormat = workbook.add_format({'bold': True, 'center_across': True})
    DataFormat = workbook.add_format({'center_across': True})
    BudgetExceedFormat = workbook.add_format({'bold': True, 'center_across': True, 'font_color': 'red'})
    Expectedbudgetformat = workbook.add_format({'bold': True, 'center_across': True, 'font_color': 'black'})

    HUBreakdown.set_column(0, 0, 40)  # width of first column - HostGroupName
    HUBreakdown.set_column(1, 1, 20)  # width of second column - HostUnits
    HUBreakdown.set_column(2, 1, 20)  # width of second column - Exp HostUnits
    HUBreakdown.write_row(0, 0, ["HostGroupName", "Consumed HostUnits", "Expected HostUnits"], TitleFormat)

    # Write Host Units
    row = 1
    hutotal = 0
    huexp = 0
    hostgrouptohudict = hu.host_units(tenantURL, token)
    tenant_HUBudget = {}
    tenant_HUBudget = prop.Tenant_HUbudget

    budgetexceededFlag = False

    budgetexceedHG = {}
    expectedHG = {}
    i = 1
    for key, val in sorted(hostgrouptohudict.items()):
        format = DataFormat
        if key in tenant_HUBudget:

            if hostgrouptohudict[key] > tenant_HUBudget[key]:
                # print("budget Exceeded " + key)
                budgetexceedHG.update({key: hostgrouptohudict[key]})
                # HUBreakdown.write_row(row, 0, [key, val],BudgetExceedFormat)
                format = BudgetExceedFormat
                budgetexceededFlag = True

        HUBreakdown.write_row(row, 0, [key, val], format)
        hutotal = hutotal + val
        row += 1

    for key, val in sorted(tenant_HUBudget.items()):
        expectedHG.update({key: tenant_HUBudget[key]})
        format = Expectedbudgetformat
        HUBreakdown.write_row(i, 2, [val], format)
        huexp = huexp + val
        i += 1
    print("---hostunits Total --" + str(hutotal))
    print("---List of budgetexceedHG--" + str(budgetexceedHG))
    HUBreakdown.write_row(row, 0, ["Total HostUnits", hutotal], TitleFormat)
    HUBreakdown.write_row(row, 2, [huexp], TitleFormat)
    return budgetexceededFlag


def main_fn():
    currenttime = (datetime.now()).strftime("%d-%m-%Y_T%H%M")

    filename = "Dynatrace_HostUnits_Consumption_Report_" + str(currenttime) + ".xlsx"

    workbook = xlsxwriter.Workbook(filename)

    livetenantbudgetexceed = createexcel(TenantURL, Token, 'LiveTenant', workbook)
    workbook.close()


    print("---- All Actions completed successfully ----")



main_fn()