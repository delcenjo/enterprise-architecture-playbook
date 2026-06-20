import os
import graphviz
import matplotlib.pyplot as plt
import json
import logging
from typing import Dict, Any, List
from global_state import GlobalState

logger = logging.getLogger("Layer4_VisualEngine")
logging.basicConfig(level=logging.INFO)

class VisualEngine:
    def __init__(self, state: GlobalState):
        self.state = state
        self.output_dir = os.path.join(os.path.dirname(__file__), "..", "assets")
        self.theme_path = os.path.join(self.output_dir, "visual_theme.json")
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Load theme
        try:
            with open(self.theme_path, 'r') as f:
                themes = json.load(f)
                self.theme = themes.get("enterprise_blue")
        except:
            self.theme = {"primary": "#0A192F", "secondary": "#E8EAF6", "accent": "#1769FF", "compute_color": "#F8FAFC", "data_color": "#F1F5F9", "network_color": "#F8FAFC", "text": "#0F172A"}

    def run_layer_4(self):
        logger.info("Starting Layer 4: High-Fidelity Visual Generation...")
        self._generate_deep_arch_diagram()
        self._generate_financial_chart()
        self._generate_load_curve()
        return "Hyper-Intelligent Visual Assets Generated"

    def _generate_risk_heatmap(self):
        """
        Generates a McKinsey-style Risk Heatmap (Probability vs Impact).
        """
        risks = self.state.technical_audit
        if not risks: return

        plt.figure(figsize=(8, 8), dpi=300)
        plt.style.use('seaborn-v0_8-whitegrid')

        # Heatmap Background (Gradient)
        import numpy as np
        x = np.linspace(0, 5, 100)
        y = np.linspace(0, 5, 100)
        X, Y = np.meshgrid(x, y)
        Z = X * Y # Simple risk gradient
        
        plt.imshow(Z, extent=[0, 5, 0, 5], origin='lower', cmap='YlOrRd', alpha=0.3, aspect='auto')

        # Plot Risks
        for r in risks:
            px = r['coordinates']['x']
            py = r['coordinates']['y']
            plt.scatter(px, py, s=200, color='#0A192F', edgecolors='white', linewidth=1.5, zorder=5)
            # Label with ID or shortened name
            plt.text(px + 0.1, py + 0.1, r['name'][:15] + "...", fontsize=8, fontweight='bold', color='#0A192F')

        plt.title("Expert Technical Risk Heatmap (2026)", fontsize=16, fontweight='bold', pad=20)
        plt.xlabel("Probability (0-5)", fontsize=12)
        plt.ylabel("Impact (0-5)", fontsize=12)
        plt.xlim(0, 5.5)
        plt.ylim(0, 5.5)
        plt.grid(True, linestyle='--', alpha=0.5)

        path = os.path.join(self.output_dir, "risk_heatmap.png")
        plt.savefig(path, bbox_inches='tight')
        plt.close()
        self.state.diagrams_paths["risk_heatmap"] = path

    def _generate_deep_arch_diagram(self):
        """
        Generates a clustered VPC/Subnet diagram with security boundaries.
        """
        dot = graphviz.Digraph(comment='Institutional Architecture', format='png')
        dot.attr(dpi='300', rankdir='TB', fontname='Inter', bgcolor='white')
        dot.attr('node', shape='box', style='filled,rounded', fontname='Inter', fontsize='11', margin='0.2')
        dot.attr('edge', color='#64748b', penwidth='1.2', arrowhead='vee')

        networking = self.state.architecture.networking
        subnets = networking.get('subnets', [])

        # 1. External Traffic & Internet Gateway
        dot.node('internet', 'INTERNET', shape='cloud', color='#1769FF', fontcolor='#1769FF')
        dot.node('igw', 'Internet Gateway', shape='doublecircle', fontsize='9')
        dot.edge('internet', 'igw')

        # 2. VPC Boundary
        with dot.subgraph(name='cluster_vpc') as vpc:
            vpc.attr(label=f"VPC ({networking.get('vpc_cidr')})", style='dashed', color='#94a3b8', fontname='Inter-Bold')
            
            # Subnet Clusters
            tiers = ["public", "private", "isolated"]
            for tier in tiers:
                tier_subnets = [s for s in subnets if s['tier'] == tier]
                if not tier_subnets: continue
                
                with vpc.subgraph(name=f'cluster_{tier}') as t:
                    label = f"{tier.upper()} TIER (Security Level: {'High' if tier != 'public' else 'Standard'})"
                    t.attr(label=label, color='#CBD5E1', bgcolor='#F8FAFC' if tier == 'public' else '#F1F5F9')
                    
                    # Place components in subnets
                    for comp in self.state.architecture.components:
                        if comp.get('subnet_tier') == tier:
                            comp_label = f"{comp['name']}\n[{comp.get('instance_type', comp['type'])}]"
                            t.node(comp['name'], comp_label, fillcolor='white', color='#0A192F')

        # 3. Dynamic Wiring
        # LB -> Private Cluster
        for comp in self.state.architecture.components:
            if comp['role'] == 'edge':
                dot.edge('igw', comp['name'])
                # Connect edge to app
                for app in self.state.architecture.components:
                    if app['role'] == 'compute':
                        dot.edge(comp['name'], app['name'])
            
            if comp['role'] == 'compute':
                # Connect app to data
                for db in self.state.architecture.components:
                    if db['role'] == 'data':
                        dot.edge(comp['name'], db['name'])

        output_path = os.path.join(self.output_dir, "architecture")
        dot.render(output_path, cleanup=True)
        self.state.diagrams_paths["architecture"] = output_path + ".png"

    def _generate_financial_chart(self):
        scenarios = self.state.financial_model.scenarios
        if not scenarios: return

        plt.figure(figsize=(12, 6), dpi=300)
        plt.style.use('seaborn-v0_8-whitegrid')
        
        colors = {"Base": "#0A192F", "Optimistic": "#10B981", "Conservative": "#EF4444"}
        
        months = range(len(list(scenarios.values())[0]))
        for name, values in scenarios.items():
            plt.plot(months, [v/1000 for v in values], label=f"{name} Strategy", color=colors.get(name), linewidth=2.5)
            plt.fill_between(months, [v/1000 for v in values], alpha=0.08, color=colors.get(name))

        plt.title("Institutional Financial Projection (5-Year Cash Flow)", fontsize=16, fontweight='bold', pad=20)
        plt.xlabel("Month of Operation", fontsize=12)
        plt.ylabel("Net Value (k USD $)", fontsize=12)
        plt.legend(frameon=True, facecolor='white', borderpad=1)
        
        path = os.path.join(self.output_dir, "financial_projection.png")
        plt.savefig(path, bbox_inches='tight')
        plt.close()
        self.state.diagrams_paths["financial_projection"] = path

    def _generate_load_curve(self):
        # Using a more professional distribution
        hours = range(24)
        load = [max(10, 100 * (1 - 0.7 * (abs(h - 12) / 12)**2)) for h in hours]
        
        plt.figure(figsize=(12, 4), dpi=300)
        plt.fill_between(hours, load, color='#1769FF', alpha=0.1)
        plt.plot(hours, load, color='#1769FF', linewidth=3)
        
        plt.title("24h Transactional Load Dynamics (Predictive)", fontsize=14, loc='left', color='#0A192F')
        plt.xlabel("Business Hours")
        plt.ylabel("Concurrent Operations")
        plt.xticks(range(0, 25, 4))
        plt.grid(True, axis='y', linestyle='--', alpha=0.3)
        
        path = os.path.join(self.output_dir, "load_curve.png")
        plt.savefig(path, bbox_inches='tight')
        plt.close()
        self.state.diagrams_paths["load_curve"] = path

if __name__ == "__main__":
    pass
