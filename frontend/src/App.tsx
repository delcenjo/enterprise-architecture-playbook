import { useState } from 'react';
import axios from 'axios';
import {
  Cpu,
  Cloud,
  Layers,
  ShieldCheck,
  Activity,
  AlertCircle,
  CheckCircle2,
  FileText
} from 'lucide-react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';
import { useEffect, useRef } from 'react';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

const InputField = ({ label, value, onChange, placeholder, type = "text" }: any) => (
  <div className="space-y-2">
    <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{label}</label>
    <input
      type={type}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      className="w-full bg-slate-900/50 border border-slate-700 rounded-lg p-3 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none transition-all"
    />
  </div>
);

const SelectField = ({ label, value, onChange, options }: any) => (
  <div className="space-y-2">
    <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{label}</label>
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="w-full bg-slate-900/50 border border-slate-700 rounded-lg p-3 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none transition-all"
    >
      {options.map((opt: any) => (
        <option key={opt.value} value={opt.value}>{opt.label}</option>
      ))}
    </select>
  </div>
);
const Dashboard = ({ clientName, roadmap, onDownload }: any) => (
  <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
    <div className="flex justify-between items-center border-b border-slate-800 pb-6">
      <div>
        <h2 className="text-2xl font-bold text-white tracking-tight">Strategic Implementation Board</h2>
        <p className="text-slate-400 text-sm">Active roadmap for {clientName}</p>
      </div>
      <button
        onClick={onDownload}
        className="flex items-center gap-2 bg-blue-600 hover:bg-blue-500 text-white px-6 py-2.5 rounded-xl font-bold transition-all shadow-lg shadow-blue-500/20 active:scale-95"
      >
        <FileText className="w-4 h-4" />
        Download Enterprise Package
      </button>
    </div>

    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <div className="lg:col-span-2 space-y-6">
        <div className="bg-slate-900/80 border border-slate-800 p-8 rounded-3xl shadow-2xl relative overflow-hidden">
          <div className="absolute top-0 right-0 p-4 opacity-5">
            <Activity className="w-32 h-32 text-blue-400" />
          </div>
          <h3 className="text-lg font-bold text-slate-100 mb-8 flex items-center gap-2">
            <Layers className="w-5 h-5 text-blue-500" />
            18-Month Transformation Timeline
          </h3>

          <div className="relative border-l-2 border-slate-800 ml-4 space-y-12 pb-4">
            {roadmap.map((step: any, idx: number) => (
              <div key={idx} className="relative pl-10 group">
                <div className={cn(
                  "absolute left-[-9px] top-0 w-4 h-4 rounded-full border-4 border-slate-900 transition-all duration-500 group-hover:scale-125",
                  step.status === 'done' ? 'bg-emerald-500 shadow-[0_0_15px_rgba(16,185,129,0.5)]' :
                    step.status === 'active' ? 'bg-blue-500 shadow-[0_0_15px_rgba(59,130,246,0.5)] animate-pulse' : 'bg-slate-700'
                )} />
                <div className="space-y-1">
                  <div className="flex items-center gap-3">
                    <span className="text-[10px] font-bold text-blue-500 tracking-widest uppercase">{step.period}</span>
                    <h4 className="text-sm font-bold text-slate-200">{step.title}</h4>
                  </div>
                  <p className="text-xs text-slate-400 leading-relaxed max-w-lg">{step.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="space-y-6">
        <div className="bg-indigo-900/20 border border-indigo-500/30 p-6 rounded-2xl">
          <h3 className="text-sm font-bold text-indigo-300 uppercase tracking-widest mb-4 flex items-center gap-2">
            <ShieldCheck className="w-4 h-4" />
            Strategic Nudges
          </h3>
          <div className="space-y-4">
            <div className="bg-indigo-500/10 border border-indigo-500/20 p-4 rounded-xl space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-bold text-indigo-400">ACTION REQUIRED</span>
                <AlertCircle className="w-3 h-3 text-indigo-400" />
              </div>
              <p className="text-xs text-indigo-100 font-medium">Month 3 Checklist: Verify Audit Trail integrity with local DORA auditors.</p>
            </div>
            <div className="bg-slate-800/50 p-4 rounded-xl">
              <p className="text-[10px] text-slate-500 uppercase font-bold mb-1 tracking-tighter">Next Milestone</p>
              <p className="text-xs text-slate-300">Phase 2: Regional VPC Deployment</p>
            </div>
          </div>
        </div>

        <div className="bg-slate-900/50 border border-slate-800 p-6 rounded-2xl">
          <h4 className="text-xs font-bold text-slate-400 uppercase mb-4">Project Integrity</h4>
          <div className="flex items-center gap-4 p-3 bg-emerald-500/5 border border-emerald-500/20 rounded-xl">
            <CheckCircle2 className="w-5 h-5 text-emerald-500" />
            <div>
              <p className="text-xs font-bold text-emerald-100 uppercase tracking-tighter">SAGA Sealed</p>
              <p className="text-[10px] text-emerald-500/70 font-mono">SHA256:8479...INMU</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
);

export default function DocumentForgeApp() {
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [workflowId, setWorkflowId] = useState<string | null>(null);
  const [workflowStatus, setWorkflowStatus] = useState<any>(null);
  const pollingInterval = useRef<any>(null);

  const [formData, setFormData] = useState({
    client_name: 'StrategicCorp',
    project_name: 'Cloud ROI Transformation',
    project_context: {
      company_type: 'Enterprise',
      industry: 'Fintech',
      countries_of_operation: 'España, France',
      product_phase: 'Scaling'
    },
    current_architecture: {
      architecture_type: 'Monolith',
      cloud_provider: 'AWS',
      tenancy_model: 'Single-tenant',
      primary_database: 'PostgreSQL',
      messaging_system: 'None',
      observability_level: 'Basic',
      cicd_maturity: 'Manual'
    },
    scale_and_load: {
      monthly_active_users: '50000',
      peak_concurrent_users: '1500',
      estimated_rps: '120.0',
      current_p95_latency_ms: '350.0',
      expected_mom_growth_pct: '10.0',
      active_regions: '1',
      target_sla: '99.99%'
    },
    data_and_sensitivity: {
      processes_pii: true,
      special_categories: false,
      processes_payments: true,
      regulated_entity: true,
      data_retention_years: '10.0',
      cross_border_transfers: false
    },
    team_and_organization: {
      total_developers: '25',
      total_sre_devops: '2',
      has_platform_team: false,
      average_seniority: 'Mid',
      deployment_frequency: 'Weekly',
      approximate_mttr: 'Hours'
    },
    financials: {
      annual_revenue: '5000000.0',
      monthly_burn_rate: '200000.0',
      cloud_cost_pct_of_revenue: '8.0',
      cac: '150.0',
      churn_rate_pct: '3.0',
      gross_margin_pct: '80.0'
    },
    user_objectives: {
      strategic_goals: 'Escalar sin romper, Prepararse para auditoría',
      primary_problem_description: 'We need to break the monolith to satisfy scaling constraints.'
    },
    advanced_overrides: ''
  });

  const startWorkflow = async () => {
    setLoading(true);
    setError(null);
    setSuccess(false);
    setWorkflowStatus({ current_status: 'EXTRACTING' });

    try {
      const response = await axios.post('http://localhost:8003/workflow/start', {
        client_name: formData.client_name,
        project_name: formData.project_name,
        project_context: {
          ...formData.project_context,
          countries_of_operation: formData.project_context.countries_of_operation.split(',').map(s => s.trim())
        },
        current_architecture: formData.current_architecture,
        scale_and_load: {
          monthly_active_users: parseInt(formData.scale_and_load.monthly_active_users),
          peak_concurrent_users: parseInt(formData.scale_and_load.peak_concurrent_users),
          estimated_rps: parseFloat(formData.scale_and_load.estimated_rps),
          current_p95_latency_ms: parseFloat(formData.scale_and_load.current_p95_latency_ms),
          expected_mom_growth_pct: parseFloat(formData.scale_and_load.expected_mom_growth_pct),
          active_regions: parseInt(formData.scale_and_load.active_regions),
          target_sla: formData.scale_and_load.target_sla
        },
        data_and_sensitivity: {
          ...formData.data_and_sensitivity,
          data_retention_years: parseFloat(formData.data_and_sensitivity.data_retention_years)
        },
        team_and_organization: {
          ...formData.team_and_organization,
          total_developers: parseInt(formData.team_and_organization.total_developers),
          total_sre_devops: parseInt(formData.team_and_organization.total_sre_devops)
        },
        financials: {
          annual_revenue: parseFloat(formData.financials.annual_revenue),
          monthly_burn_rate: parseFloat(formData.financials.monthly_burn_rate),
          cloud_cost_pct_of_revenue: parseFloat(formData.financials.cloud_cost_pct_of_revenue),
          cac: parseFloat(formData.financials.cac),
          churn_rate_pct: parseFloat(formData.financials.churn_rate_pct),
          gross_margin_pct: parseFloat(formData.financials.gross_margin_pct)
        },
        user_objectives: {
          strategic_goals: formData.user_objectives.strategic_goals.split(',').map(s => s.trim()),
          primary_problem_description: formData.user_objectives.primary_problem_description
        },
        advanced_overrides: formData.advanced_overrides
      });

      setWorkflowId(response.data.workflow_id);
    } catch (err: any) {
      console.error(err);
      setError("Error al iniciar el workflow. Verifica la conexión.");
      setLoading(false);
    }
  };

  const approveWorkflow = async () => {
    if (!workflowId) return;
    try {
      await axios.post(`http://localhost:8003/workflow/${workflowId}/approve`);
    } catch (err: any) {
      setError("Error al aprobar el workflow.");
    }
  };

  useEffect(() => {
    if (workflowId) {
      pollingInterval.current = setInterval(async () => {
        try {
          const resp = await axios.get(`http://localhost:8003/workflow/${workflowId}`);
          setWorkflowStatus(resp.data);

          if (resp.data.current_status === 'COMPLETED') {
            clearInterval(pollingInterval.current);
            setLoading(false);
            setSuccess(true);
          }
          if (resp.data.current_status === 'ERROR') {
            clearInterval(pollingInterval.current);
            setLoading(false);
            setError("Pipeline crashed.");
          }
        } catch (e) {
          console.error("Polling error", e);
        }
      }, 2000);
    }
    return () => clearInterval(pollingInterval.current);
  }, [workflowId]);

  const downloadPackage = async () => {
    if (!workflowStatus?.metadata?.sections) return;
    try {
      const resp = await axios.post('http://localhost:8002/generate-dossier', {
        client_name: formData.client_name,
        project_name: formData.project_name,
        sections: workflowStatus.metadata.sections
      }, { responseType: 'blob' });

      const url = window.URL.createObjectURL(new Blob([resp.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `Dossier_${formData.client_name.replace(/\s+/g, '_')}.zip`);
      document.body.appendChild(link);
      link.click();
    } catch (err: any) {
      setError("Error al descargar el paquete de consultoría.");
    }
  };


  const showDashboard = success && workflowStatus?.current_status === 'COMPLETED';

  return (
    <div className="min-h-screen bg-[#0d1117] text-slate-200 font-sans p-6 md:p-12">
      <header className="max-w-6xl mx-auto flex items-center justify-between mb-16">
        <div className="flex items-center gap-4">
          <div className="bg-blue-600 p-2.5 rounded-xl shadow-[0_0_20px_rgba(37,99,235,0.4)]">
            <Cpu className="w-8 h-8 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold tracking-tight bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">
              Architecture Playbook
            </h1>
            <p className="text-xs text-slate-500 font-medium tracking-[0.2em] uppercase">Architecture Decision Engine</p>
          </div>
        </div>

        <div className="hidden md:flex items-center gap-6 text-sm font-medium text-slate-400">
          <div className="flex items-center gap-2 px-4 py-2 bg-slate-800/50 rounded-full border border-slate-700">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            <span>Deterministic Core V4.0</span>
          </div>
          <div className="flex items-center gap-2">
            <Activity className="w-4 h-4 text-blue-400" />
            <span>Operational</span>
          </div>
        </div>
      </header>

      {showDashboard ? (
        <main className="max-w-6xl mx-auto">
          <Dashboard
            clientName={formData.client_name}
            onDownload={downloadPackage}
            roadmap={[
              { period: 'Month 0-3', title: 'Foundation & Compliance', desc: 'Secure landing zones, audit trail deployment, and DORA alignment.', status: 'done' },
              { period: 'Month 4-9', title: 'Core Migration', desc: 'Lifting detected stack to serverless/k8s high-availability clusters.', status: 'active' },
              { period: 'Month 10-18', title: 'Edge Intelligence', desc: 'Deployment of operational AI agents for real-time cost control.', status: 'pending' },
            ]}
          />
        </main>
      ) : (
        <main className="max-w-6xl mx-auto grid lg:grid-cols-2 gap-12 items-start">

          <section className="space-y-8 animate-in fade-in slide-in-from-left-4 duration-700">
            <div className="space-y-2">
              <h2 className="text-4xl font-extrabold tracking-tight text-white">
                Orchestrate your <span className="text-blue-500">Deliverable.</span>
              </h2>
              <p className="text-slate-400 text-lg">
                Generate financial simulations, architectures and interactive dashboards in seconds.
              </p>
            </div>

            <div className="bg-slate-900 border border-slate-800 p-8 rounded-2xl shadow-2xl space-y-6 relative overflow-hidden group">
              <div className="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity">
                <Layers className="w-32 h-32" />
              </div>

              <div className="grid md:grid-cols-2 gap-6">
                <InputField
                  label="Client Name"
                  value={formData.client_name}
                  onChange={(v: string) => setFormData({ ...formData, client_name: v })}
                  placeholder="e.g. Acme Corp"
                />
                <InputField
                  label="Project Name"
                  value={formData.project_name}
                  onChange={(v: string) => setFormData({ ...formData, project_name: v })}
                  placeholder="e.g. Migration 2026"
                />
              </div>

              <div className="space-y-8">
                <div className="space-y-4">
                  <h3 className="text-sm font-bold text-slate-300 uppercase tracking-widest border-b border-slate-700 pb-2">1. Project Context</h3>
                  <div className="grid md:grid-cols-2 gap-4">
                    <SelectField
                      label="Company Type"
                      value={formData.project_context.company_type}
                      onChange={(v: string) => setFormData({ ...formData, project_context: { ...formData.project_context, company_type: v } })}
                      options={[{ label: "Startup", value: "Startup" }, { label: "Scale-up", value: "Scale-up" }, { label: "Enterprise", value: "Enterprise" }, { label: "Regulated Entity", value: "Regulated" }]}
                    />
                    <SelectField
                      label="Industry"
                      value={formData.project_context.industry}
                      onChange={(v: string) => setFormData({ ...formData, project_context: { ...formData.project_context, industry: v } })}
                      options={[{ label: "Fintech", value: "Fintech" }, { label: "Healthtech", value: "Healthtech" }, { label: "SaaS", value: "SaaS" }, { label: "E-commerce", value: "E-commerce" }, { label: "General", value: "General" }]}
                    />
                    <InputField
                      label="Operations (CSV)"
                      value={formData.project_context.countries_of_operation}
                      onChange={(v: string) => setFormData({ ...formData, project_context: { ...formData.project_context, countries_of_operation: v } })}
                      placeholder="España, EU, US"
                    />
                    <SelectField
                      label="Product Phase"
                      value={formData.project_context.product_phase}
                      onChange={(v: string) => setFormData({ ...formData, project_context: { ...formData.project_context, product_phase: v } })}
                      options={[{ label: "MVP", value: "MVP" }, { label: "PMF", value: "PMF" }, { label: "Scaling", value: "Scaling" }, { label: "Enterprise-grade", value: "Enterprise-grade" }]}
                    />
                  </div>
                </div>

                <div className="space-y-4">
                  <h3 className="text-sm font-bold text-slate-300 uppercase tracking-widest border-b border-slate-700 pb-2">2. Current Architecture</h3>
                  <div className="grid md:grid-cols-2 gap-4">
                    <SelectField
                      label="Architecture Type"
                      value={formData.current_architecture.architecture_type}
                      onChange={(v: string) => setFormData({ ...formData, current_architecture: { ...formData.current_architecture, architecture_type: v } })}
                      options={[{ label: "Monolith", value: "Monolith" }, { label: "Microservices", value: "Microservices" }, { label: "Serverless", value: "Serverless" }]}
                    />
                    <SelectField
                      label="Cloud Provider"
                      value={formData.current_architecture.cloud_provider}
                      onChange={(v: string) => setFormData({ ...formData, current_architecture: { ...formData.current_architecture, cloud_provider: v } })}
                      options={[{ label: "AWS", value: "AWS" }, { label: "GCP", value: "GCP" }, { label: "Azure", value: "Azure" }, { label: "On-prem", value: "On-prem" }]}
                    />
                    <SelectField
                      label="CI/CD Maturity"
                      value={formData.current_architecture.cicd_maturity}
                      onChange={(v: string) => setFormData({ ...formData, current_architecture: { ...formData.current_architecture, cicd_maturity: v } })}
                      options={[{ label: "Manual", value: "Manual" }, { label: "Semi-automated", value: "Semi-automated" }, { label: "GitOps", value: "GitOps" }]}
                    />
                    <InputField
                      label="Primary DB"
                      value={formData.current_architecture.primary_database}
                      onChange={(v: string) => setFormData({ ...formData, current_architecture: { ...formData.current_architecture, primary_database: v } })}
                    />
                  </div>
                </div>

                <div className="space-y-4">
                  <h3 className="text-sm font-bold text-slate-300 uppercase tracking-widest border-b border-slate-700 pb-2">3. Strategic Objectives</h3>
                  <InputField
                    label="Strategic Goals (CSV)"
                    value={formData.user_objectives.strategic_goals}
                    onChange={(v: string) => setFormData({ ...formData, user_objectives: { ...formData.user_objectives, strategic_goals: v } })}
                    placeholder="Escalar sin romper, Levantar ronda, Prepararse para auditoría..."
                  />
                  <InputField
                    label="Primary Problem"
                    value={formData.user_objectives.primary_problem_description}
                    onChange={(v: string) => setFormData({ ...formData, user_objectives: { ...formData.user_objectives, primary_problem_description: v } })}
                    placeholder="We need to migrate to K8s to reduce costs..."
                  />
                </div>

                {(formData.user_objectives.strategic_goals.includes('Escalar sin romper') || parseInt(formData.scale_and_load.monthly_active_users) >= 1000000 || formData.project_context.product_phase === 'Scaling' || formData.project_context.product_phase === 'Enterprise-grade') && (
                  <div className="space-y-4 animate-in fade-in zoom-in duration-500 bg-blue-900/10 p-5 border border-blue-500/20 rounded-xl relative overflow-hidden">
                    <div className="absolute top-0 right-0 p-4 opacity-10">
                      <Activity className="w-16 h-16 text-blue-400" />
                    </div>
                    <h3 className="text-sm font-bold text-blue-300 uppercase tracking-widest border-b border-blue-500/30 pb-2">Deep Scaling & Load</h3>
                    <div className="grid md:grid-cols-3 gap-4">
                      <InputField label="MAU" type="number" value={formData.scale_and_load.monthly_active_users} onChange={(v: string) => setFormData({ ...formData, scale_and_load: { ...formData.scale_and_load, monthly_active_users: v } })} />
                      <InputField label="Peak Concurrent" type="number" value={formData.scale_and_load.peak_concurrent_users} onChange={(v: string) => setFormData({ ...formData, scale_and_load: { ...formData.scale_and_load, peak_concurrent_users: v } })} />
                      <InputField label="Est. RPS" type="number" value={formData.scale_and_load.estimated_rps} onChange={(v: string) => setFormData({ ...formData, scale_and_load: { ...formData.scale_and_load, estimated_rps: v } })} />
                      <InputField label="P95 Latency (ms)" type="number" value={formData.scale_and_load.current_p95_latency_ms} onChange={(v: string) => setFormData({ ...formData, scale_and_load: { ...formData.scale_and_load, current_p95_latency_ms: v } })} />
                      <InputField label="MoM Growth (%)" type="number" value={formData.scale_and_load.expected_mom_growth_pct} onChange={(v: string) => setFormData({ ...formData, scale_and_load: { ...formData.scale_and_load, expected_mom_growth_pct: v } })} />
                      <SelectField label="Target SLA" value={formData.scale_and_load.target_sla} onChange={(v: string) => setFormData({ ...formData, scale_and_load: { ...formData.scale_and_load, target_sla: v } })} options={[{ label: "99%", value: "99%" }, { label: "99.9%", value: "99.9%" }, { label: "99.99%", value: "99.99%" }]} />
                    </div>
                  </div>
                )}

                {(formData.project_context.industry === 'Fintech' && (formData.project_context.countries_of_operation.includes('España') || formData.project_context.countries_of_operation.includes('EU'))) && (
                  <div className="space-y-4 animate-in fade-in zoom-in duration-500 bg-amber-900/10 p-5 border border-amber-500/20 rounded-xl relative overflow-hidden">
                    <div className="absolute top-0 right-0 p-4 opacity-10">
                      <ShieldCheck className="w-16 h-16 text-amber-400" />
                    </div>
                    <h3 className="text-sm font-bold text-amber-300 uppercase tracking-widest border-b border-amber-500/30 pb-2 text-shadow">EU Fintech Regulation</h3>
                    <div className="grid md:grid-cols-2 gap-4">
                      <SelectField label="Processes PII?" value={formData.data_and_sensitivity.processes_pii.toString()} onChange={(v: string) => setFormData({ ...formData, data_and_sensitivity: { ...formData.data_and_sensitivity, processes_pii: v === 'true' } })} options={[{ label: "Yes (GDPR)", value: "true" }, { label: "No", value: "false" }]} />
                      <SelectField label="Processes Payments?" value={formData.data_and_sensitivity.processes_payments.toString()} onChange={(v: string) => setFormData({ ...formData, data_and_sensitivity: { ...formData.data_and_sensitivity, processes_payments: v === 'true' } })} options={[{ label: "Yes (PSD2)", value: "true" }, { label: "No", value: "false" }]} />
                      <SelectField label="Regulated Entity?" value={formData.data_and_sensitivity.regulated_entity.toString()} onChange={(v: string) => setFormData({ ...formData, data_and_sensitivity: { ...formData.data_and_sensitivity, regulated_entity: v === 'true' } })} options={[{ label: "Yes (DORA/BdE)", value: "true" }, { label: "No", value: "false" }]} />
                      <InputField label="Retention (Years)" type="number" value={formData.data_and_sensitivity.data_retention_years} onChange={(v: string) => setFormData({ ...formData, data_and_sensitivity: { ...formData.data_and_sensitivity, data_retention_years: v } })} />
                    </div>
                  </div>
                )}

                {(formData.user_objectives.strategic_goals.includes('Levantar ronda') || formData.project_context.product_phase === 'Startup' || formData.project_context.product_phase === 'Scale-up') && (
                  <div className="space-y-4 animate-in fade-in zoom-in duration-500 bg-emerald-900/10 p-5 border border-emerald-500/20 rounded-xl relative overflow-hidden">
                    <div className="absolute top-0 right-0 p-4 opacity-10">
                      <Cloud className="w-16 h-16 text-emerald-400" />
                    </div>
                    <h3 className="text-sm font-bold text-emerald-300 uppercase tracking-widest border-b border-emerald-500/30 pb-2">Financials & Burn</h3>
                    <div className="grid md:grid-cols-3 gap-4">
                      <InputField label="ARR ($)" type="number" value={formData.financials.annual_revenue} onChange={(v: string) => setFormData({ ...formData, financials: { ...formData.financials, annual_revenue: v } })} />
                      <InputField label="Monthly Burn ($)" type="number" value={formData.financials.monthly_burn_rate} onChange={(v: string) => setFormData({ ...formData, financials: { ...formData.financials, monthly_burn_rate: v } })} />
                      <InputField label="Cloud Cost (%)" type="number" value={formData.financials.cloud_cost_pct_of_revenue} onChange={(v: string) => setFormData({ ...formData, financials: { ...formData.financials, cloud_cost_pct_of_revenue: v } })} />
                      <InputField label="CAC ($)" type="number" value={formData.financials.cac} onChange={(v: string) => setFormData({ ...formData, financials: { ...formData.financials, cac: v } })} />
                      <InputField label="Churn %" type="number" value={formData.financials.churn_rate_pct} onChange={(v: string) => setFormData({ ...formData, financials: { ...formData.financials, churn_rate_pct: v } })} />
                      <InputField label="Gross Margin %" type="number" value={formData.financials.gross_margin_pct} onChange={(v: string) => setFormData({ ...formData, financials: { ...formData.financials, gross_margin_pct: v } })} />
                    </div>
                  </div>
                )}

                <div className="space-y-4">
                  <h3 className="text-sm font-bold text-slate-300 uppercase tracking-widest border-b border-slate-700 pb-2">4. Team Topology</h3>
                  <div className="grid md:grid-cols-3 gap-4">
                    <InputField label="Devs" type="number" value={formData.team_and_organization.total_developers} onChange={(v: string) => setFormData({ ...formData, team_and_organization: { ...formData.team_and_organization, total_developers: v } })} />
                    <InputField label="SRE/DevOps" type="number" value={formData.team_and_organization.total_sre_devops} onChange={(v: string) => setFormData({ ...formData, team_and_organization: { ...formData.team_and_organization, total_sre_devops: v } })} />
                    <SelectField
                      label="Platform Team?"
                      value={formData.team_and_organization.has_platform_team.toString()}
                      onChange={(v: string) => setFormData({ ...formData, team_and_organization: { ...formData.team_and_organization, has_platform_team: v === 'true' } })}
                      options={[{ label: "Yes", value: "true" }, { label: "No", value: "false" }]}
                    />
                  </div>
                </div>

                <div className="space-y-4">
                  <h3 className="text-sm font-bold text-slate-300 uppercase tracking-widest border-b border-slate-700 pb-2">5. Overrides</h3>
                  <textarea
                    value={formData.advanced_overrides || ''}
                    onChange={(e) => setFormData({ ...formData, advanced_overrides: e.target.value })}
                    placeholder="Inyectar comandos de configuración avanzada (OVERRIDE_STORAGE_GB=1000)"
                    className="w-full bg-slate-900/50 border border-slate-700 rounded-lg p-3 text-xs font-mono text-blue-300 focus:ring-2 focus:ring-blue-500 focus:outline-none transition-all h-20"
                  />
                </div>
              </div>

              <button
                onClick={startWorkflow}
                disabled={loading}
                className={cn(
                  "w-full py-4 px-6 rounded-xl font-bold flex items-center justify-center gap-3 transition-all transform active:scale-[0.98]",
                  loading
                    ? "bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700"
                    : "bg-blue-600 hover:bg-blue-500 text-white shadow-[0_0_30px_rgba(37,99,235,0.3)] hover:shadow-[0_0_40px_rgba(37,99,235,0.5)]"
                )}
              >
                {loading ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    <span>Workflow Active: {workflowStatus?.current_status || 'INITIALIZING'}</span>
                  </>
                ) : (
                  <>
                    <Layers className="w-5 h-5" />
                    <span>Trigger 5-Layer Orchestration</span>
                  </>
                )}
              </button>

              {workflowStatus?.current_status === 'PENDING_HUMAN' && (
                <div className="p-6 bg-amber-500/5 border border-amber-500/20 rounded-2xl space-y-4 animate-in slide-in-from-top-4 duration-500">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3 text-amber-400">
                      <ShieldCheck className="w-6 h-6" />
                      <h4 className="font-bold">Human-in-the-Loop Approval Required</h4>
                    </div>
                    <span className="text-[10px] bg-amber-500/20 text-amber-500 px-2 py-0.5 rounded font-bold uppercase">Capa 4</span>
                  </div>
                  <p className="text-sm text-slate-400 italic">
                    "Compliance Analysis generation completed. Identified 2 regulatory gaps (DORA). Review draft before finalization."
                  </p>
                  <div className="bg-slate-900/80 p-3 rounded-lg border border-slate-800 text-xs font-mono text-slate-500 max-h-24 overflow-hidden mb-4">
                    {JSON.stringify(workflowStatus.metadata)}
                  </div>
                  <button
                    onClick={approveWorkflow}
                    className="w-full bg-amber-500 hover:bg-amber-400 text-black font-bold py-3 rounded-xl transition-colors"
                  >
                    Approve Intelligence Section
                  </button>
                </div>
              )}


              {success && (
                <div className="flex items-center gap-3 p-4 bg-emerald-500/10 border border-emerald-500/20 rounded-xl text-emerald-400 animate-in fade-in zoom-in duration-300">
                  <CheckCircle2 className="w-5 h-5" />
                  <span className="text-sm font-medium">Artifact package generated and downloaded successfully.</span>
                </div>
              )}

              {error && (
                <div className="flex items-center gap-3 p-4 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400 animate-in shake duration-500">
                  <AlertCircle className="w-5 h-5" />
                  <span className="text-sm font-medium">{error}</span>
                </div>
              )}
            </div>
          </section>

          <section className="space-y-6 lg:mt-12 animate-in fade-in slide-in-from-right-4 duration-1000">
            <div className="grid sm:grid-cols-2 gap-4">
              <FeatureCard
                icon={<FileText className="text-blue-500" />}
                title="30+ Page PDF"
                desc="Comprehensive architectural analysis and executive summary."
              />
              <FeatureCard
                icon={<Cloud className="text-indigo-500" />}
                title="Infrastructure"
                desc="Ready-to-deploy Terraform code based on selected region."
              />
              <FeatureCard
                icon={<Activity className="text-emerald-500" />}
                title="ROI Simulation"
                desc="Interactive dashboard with real NPV and TCO calculations."
              />
              <FeatureCard
                icon={<ShieldCheck className="text-slate-500" />}
                title="ADR Records"
                desc="Formal decision records for architectural compliance."
              />
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 overflow-hidden relative group">
              <div className="flex justify-between items-center mb-6">
                <h3 className="text-sm font-bold text-slate-400 uppercase tracking-widest">Live Orchestration Feed</h3>
                <span className={cn("flex h-2 w-2 rounded-full animate-pulse", loading ? "bg-blue-500" : "bg-emerald-500")}></span>
              </div>
              <div className="space-y-4 font-mono text-[10px]">
                <div className="flex transition-all duration-500 gap-3">
                  <span className={cn("px-2 py-0.5 rounded", workflowStatus?.current_status === 'EXTRACTING' ? "bg-blue-500/20 text-blue-400" : "text-slate-600")}>C3_PARSER</span>
                  <p className={workflowStatus?.current_status === 'EXTRACTING' ? "text-blue-400" : "text-slate-600"}>[EXTRACTING] Analyzing technology stack signatures...</p>
                </div>
                <div className="flex transition-all duration-500 gap-3">
                  <span className={cn("px-2 py-0.5 rounded", workflowStatus?.current_status === 'REASONING' ? "bg-indigo-500/20 text-indigo-400" : "text-slate-600")}>C2_GRAPH</span>
                  <p className={workflowStatus?.current_status === 'REASONING' ? "text-indigo-400" : "text-slate-600"}>[KNOWLEDGE] Deep lookup for DORA articles in: {formData.current_architecture.cloud_provider}</p>
                </div>
                <div className="flex transition-all duration-500 gap-3">
                  <span className={cn("px-2 py-0.5 rounded", workflowStatus?.current_status === 'PENDING_HUMAN' ? "bg-amber-500/20 text-amber-400" : "text-slate-600")}>C4_CORE</span>
                  <p className={workflowStatus?.current_status === 'PENDING_HUMAN' ? "text-amber-400" : "text-slate-600"}>[STATE] Human-in-the-loop: Awaiting Expert Validation...</p>
                </div>
                <div className="border-t border-slate-800 pt-3 mt-2">
                  <p className="text-slate-500 uppercase text-[9px] mb-2 font-bold tracking-widest">Nudges (Next Milestones)</p>
                  <div className="space-y-2">
                    <div className="flex items-start gap-2 text-slate-400 group/nudge">
                      <CheckCircle2 className="w-3 h-3 mt-0.5 text-slate-600 group-hover/nudge:text-emerald-500" />
                      <span>Hito 1: Compliance DORA verificado para el stack AWS.</span>
                    </div>
                    <div className="flex items-start gap-2 text-slate-400 group/nudge">
                      <Activity className="w-3 h-3 mt-0.5 text-slate-600 group-hover/nudge:text-blue-500" />
                      <span>Nudge [Mes 3]: Iniciar proceso de certificación ISO 27001.</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

          </section>

        </main>
      )}

      <footer className="mt-24 pt-8 border-t border-slate-800/50 max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-center gap-4 text-slate-500 text-xs font-medium uppercase tracking-[0.2em]">
        <span>© 2026</span>
        <span className="bg-slate-900 px-3 py-1 rounded">Live</span>
        <div className="flex gap-4">
          <span className="hover:text-white cursor-pointer transition-colors">Documentation</span>
          <span className="hover:text-white cursor-pointer transition-colors">API Keys</span>
        </div>
      </footer>
    </div>
  );
}

function FeatureCard({ icon, title, desc }: any) {
  return (
    <div className="bg-slate-900/40 border border-slate-800 p-6 rounded-2xl hover:border-slate-700 transition-all hover:translate-y-[-4px] cursor-default group">
      <div className="mb-4 transform transition-transform group-hover:scale-110 duration-300">{icon}</div>
      <h4 className="text-white font-bold mb-1">{title}</h4>
      <p className="text-slate-500 text-xs leading-relaxed">{desc}</p>
    </div>
  );
}
