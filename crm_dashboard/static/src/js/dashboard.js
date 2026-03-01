/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
const { Component, onWillStart, useState ,useRef,onMounted} = owl;
import { loadJS } from "@web/core/assets";

export class CrmDashboard extends Component {
    setup() {
        console.log("this",this)
        this.chartRef = useRef("chart");

        this.action = useService("action");
        this.orm = useService("orm");
        console.log("this action",this.action)
        console.log("this orm",this.orm)

        this.state = useState({
            data: {},
            period: "year",
            isManager: false,
        });
        console.log("data",this.state.data)

        onWillStart(async () => {
            await this.loadData();
        });
         onMounted(() => {
            this.activityChart();
            this.mediumChart();
            this.campaignChart();
            this.lostChart();

        });

}

lostChart() {
        const data = this.state.lost;
        const labels = data.map(m => m.id[0]);
        const counts = data.map(m => m.expected_revenue);
        const ctx = document.getElementById('lostChart');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Leads',
                    data: counts,
                    backgroundColor: [
                        '#ff6384', '#36a2eb', '#cc65fe', '#ffce56', '#2ecc71'
                    ],
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                    }
                }
            }
        });
    }

activityChart() {
//    const ctx = document.getElementById('activityChart-' + this.state.id).getContext('2d');
     const ctx = document.getElementById('activityChart');

    const labels = this.state.activities.map(m => m.activity_type_id[1]);
    const data = this.state.activities.map(m => m.activity_type_id_count);

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0']
            }]
        }
    });
}
 mediumChart() {
        const data = this.state.leadsByMedium;
        const labels = data.map(m => m.medium_id[1]);
        const counts = data.map(m => m.medium_id_count);

        const ctx = document.getElementById('leadsByMediumChart');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Leads',
                    data: counts,
                    backgroundColor: [
                        '#ff6384', '#36a2eb', '#cc65fe', '#ffce56', '#2ecc71'
                    ],
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                    }
                }
            }
        });
    }
    campaignChart() {
        const data1 = this.state.leadsByCampaign;
        const labels = data1.map(m => m.campaign_id[1]);
        const counts = data1.map(m => m.campaign_id_count);

        const ctx = document.getElementById('leadsByCampaignChart');
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Leads',
                    data: counts,
                    backgroundColor: [
                        '#ff6384', '#36a2eb', '#cc65fe', '#ffce56', '#2ecc71'
                    ],
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                    }
                }
            }
        });
    }

    async loadData() {

        const result = await this.orm.call("crm.lead", "get_crm_dashboard_data",[this.state.period]);
        this.state.lost = await this.orm.call("crm.lead", "get_lost_data", []);
        this.state.leadsByMonth = await this.orm.call("crm.lead", "get_leads_by_month", []);
        this.state.activities = await this.orm.call("crm.lead", "get_activity_pie", []);
        this.state.leadsByMedium = await this.orm.call("crm.lead", "get_leads_by_medium", []);
        this.state.leadsByCampaign = await this.orm.call("crm.lead", "get_leads_by_campaign", []);

        console.log("result",result)
        console.log("lost",this.state.lost)
        console.log("leads by month",this.state.leadsByMonth)
        console.log("activities",this.state.activities)
        console.log("leads by medium",this.state.leadsByMedium)
        console.log("leads by campaign",this.state.leadsByCampaign)

        console.log(" period",this.state.period)
        this.state.data = result;
        this.state.leads = result.leads
        console.log("new data",this.state.data)
        this.user = result.user;
        console.log("user",this.user)
        this.state.isManager = result.is_manager;
        console.log("is manager??",this.state.isManager)
    }

    async setPeriod(period) {
        this.state.period = period;
        console.log("new period",this.state.period)
        await this.loadData();
    }

    async openView(type) {

        const result = await this.orm.call("crm.lead", "get_crm_dashboard_data",[this.state.period]);
//        let domain = [];
        let domain = result.domain;
        console.log("domain",domain)
//        if (!this.state.isManager) {
//            domain.push(["user_id", "=", this.user]);
//        }

        this.action.doAction({
            type: "ir.actions.act_window",
            name: type === "lead" ? "My Leads" : "My Opportunities",
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
            domain: [...domain, ["type", "=", type]],
        });
    }

    async openmanView(type) {

        const result = await this.orm.call("crm.lead", "get_crm_dashboard_data",[this.state.period]);
        console.log("leads",result.leads)
        let domain2 = result.domain2;
        console.log("domain2",domain2)

        this.action.doAction({
            type: "ir.actions.act_window",
            name: type === "lead" ? "My Leads" : "My Opportunities",
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
            domain: [...domain2, ["type", "=", type]],
        });
    }

    openLead(leadId) {

    this.action.doAction({
        type: "ir.actions.act_window",
        res_model: "crm.lead",
        res_id: leadId,
        views: [[false, "form"]],
        target: "current",
    });
}




}

CrmDashboard.template = "crm_dashboard.CrmDashboard";
registry.category("actions").add("crm_dashboard_tag", CrmDashboard);

