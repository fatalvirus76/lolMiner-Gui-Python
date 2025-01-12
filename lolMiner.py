import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os

class LolMinerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("lolMiner GUI")
        self.root.geometry("800x1000")

        # Coin, Algorithm, and Wallet Selection
        self.create_coin_algorithm_wallet_section()

        # General Configuration
        self.create_general_configuration_section()

        # Mining Options
        self.create_mining_options_section()

        # Pool Settings
        self.create_pool_settings_section()

        # Device Configuration
        self.create_device_configuration_section()

        # Mining Monitor and API
        self.create_monitor_api_section()

        # Benchmark Button
        self.create_benchmark_section()

        # Stop Buttons
        self.create_stop_buttons()

        # Run Button
        self.run_button = tk.Button(self.root, text="Start lolMiner", command=self.run_lolminer)
        self.run_button.grid(row=22, column=0, columnspan=2, pady=20)

    def create_coin_algorithm_wallet_section(self):
        # Coin Dropdown
        self.coin_label = tk.Label(self.root, text="Select Coin:")
        self.coin_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.coin_choices = [''] + ['AION', 'AUTO144_5', 'AUTO192_7', 'BEAM', 'BTCZ', 'BTG', 'ETC', 'ETH', 'CTXC', 'EXCC', 'GRIN-C29M', 'GRIN-C32', 'MWC-C29D', 'MWC-C31', 'XSG', 'YEC', 'ZCL', 'ZEL', 'ZER']
        self.coin_dropdown = ttk.Combobox(self.root, values=self.coin_choices)
        self.coin_dropdown.grid(row=0, column=1, padx=10, pady=10)

        # Algorithm Dropdown
        self.algorithm_label = tk.Label(self.root, text="Set Algorithm:")
        self.algorithm_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        self.algorithm_choices = ["", "AUTOLYKOS2", "BEAM-III", "C29AE", "C29D", "C29M", "C30CTX", "C31", "C32", "CR29-32", "CR29-40", "CR29-48", "EQUI144_5", "EQUI192_7", "EQUI210_9", "ETCHASH", "ETHASH", "ZEL"]
        self.algorithm_dropdown = ttk.Combobox(self.root, values=self.algorithm_choices)
        self.algorithm_dropdown.grid(row=0, column=3, padx=10, pady=10)

        # Wallet Address
        self.wallet_label = tk.Label(self.root, text="Wallet Address:")
        self.wallet_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.wallet_entry = tk.Entry(self.root)
        self.wallet_entry.insert(0, "38bj4uu8uDsnC5NjoeGb8TMviBCEtMiaet")
        self.wallet_entry.grid(row=1, column=1, padx=10, pady=10)

    def create_general_configuration_section(self):
        # Balance
        self.balance_label = tk.Label(self.root, text="Balance Amount:")
        self.balance_label.grid(row=1, column=2, padx=10, pady=10, sticky="w")

        self.balance_entry = tk.Entry(self.root)
        self.balance_entry.grid(row=1, column=3, padx=10, pady=10)

        # Show Version
        self.version_var = tk.IntVar()
        self.version_check = tk.Checkbutton(self.root, text="Show Version", variable=self.version_var)
        self.version_check.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def create_mining_options_section(self):
        # CPU Mining
        self.cpu_var = tk.IntVar()
        self.cpu_check = tk.Checkbutton(self.root, text="Use Only CPU Mining", variable=self.cpu_var)
        self.cpu_check.grid(row=2, column=2, columnspan=2, padx=10, pady=10)

        # GPU ID
        self.gpu_id_label = tk.Label(self.root, text="GPU ID:")
        self.gpu_id_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.gpu_id_entry = tk.Entry(self.root)
        self.gpu_id_entry.grid(row=3, column=1, padx=10, pady=10)

        # Force Fan
        self.force_fan_var = tk.IntVar()
        self.force_fan_check = tk.Checkbutton(self.root, text="Force Fan Control", variable=self.force_fan_var)
        self.force_fan_check.grid(row=3, column=2, columnspan=2, padx=10, pady=10)

        # Memory Allocation
        self.mem_alloc_label = tk.Label(self.root, text="Memory Allocation Size:")
        self.mem_alloc_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        self.mem_alloc_entry = tk.Entry(self.root)
        self.mem_alloc_entry.grid(row=4, column=1, padx=10, pady=10)

        # Retries
        self.retries_label = tk.Label(self.root, text="Number of Retries:")
        self.retries_label.grid(row=4, column=2, padx=10, pady=10, sticky="w")

        self.retries_entry = tk.Entry(self.root)
        self.retries_entry.grid(row=4, column=3, padx=10, pady=10)

        # Timeout
        self.timeout_label = tk.Label(self.root, text="Timeout (seconds):")
        self.timeout_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")

        self.timeout_entry = tk.Entry(self.root)
        self.timeout_entry.grid(row=5, column=1, padx=10, pady=10)

    def create_pool_settings_section(self):
        # Pool Query URL
        self.pool_query_label = tk.Label(self.root, text="Pool Query URL:")
        self.pool_query_label.grid(row=5, column=2, padx=10, pady=10, sticky="w")

        self.pool_query_entry = tk.Entry(self.root)
        self.pool_query_entry.grid(row=5, column=3, padx=10, pady=10)

        # Pool Server
        self.pool_label = tk.Label(self.root, text="Pool URL:")
        self.pool_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")

        self.pool_entry = tk.Entry(self.root)
        self.pool_entry.insert(0, "stratum+tcp://etchash.auto.nicehash.com:9200")
        self.pool_entry.grid(row=6, column=1, padx=10, pady=10)

        # Kill on Die
        self.kill_on_die_var = tk.IntVar()
        self.kill_on_die_check = tk.Checkbutton(self.root, text="Kill Miner on GPU Death", variable=self.kill_on_die_var)
        self.kill_on_die_check.grid(row=6, column=2, columnspan=2, padx=10, pady=10)

    def create_device_configuration_section(self):
        # Device Name
        self.device_label = tk.Label(self.root, text="Device Name:")
        self.device_label.grid(row=7, column=0, padx=10, pady=10, sticky="w")

        self.device_entry = tk.Entry(self.root)
        self.device_entry.grid(row=7, column=1, padx=10, pady=10)

        # Max Devices
        self.max_devices_var = tk.IntVar()
        self.max_devices_check = tk.Checkbutton(self.root, text="Use Max Devices", variable=self.max_devices_var)
        self.max_devices_check.grid(row=7, column=2, columnspan=2, padx=10, pady=10)

        # No Dual Accounts
        self.no_dual_accounts_var = tk.IntVar()
        self.no_dual_accounts_check = tk.Checkbutton(self.root, text="Disable Dual Accounts", variable=self.no_dual_accounts_var)
        self.no_dual_accounts_check.grid(row=8, column=0, columnspan=4, padx=10, pady=10)

    def create_monitor_api_section(self):
        # Close All Miners
        self.close_miners_var = tk.IntVar()
        self.close_miners_check = tk.Checkbutton(self.root, text="Close All Miners", variable=self.close_miners_var)
        self.close_miners_check.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

        # Watch Miner
        self.watch_label = tk.Label(self.root, text="Watch Miner:")
        self.watch_label.grid(row=9, column=2, padx=10, pady=10, sticky="w")

        self.watch_entry = tk.Entry(self.root)
        self.watch_entry.grid(row=9, column=3, padx=10, pady=10)

        # API Key
        self.api_label = tk.Label(self.root, text="API Key:")
        self.api_label.grid(row=10, column=0, padx=10, pady=10, sticky="w")

        self.api_entry = tk.Entry(self.root)
        self.api_entry.grid(row=10, column=1, padx=10, pady=10)

    def create_benchmark_section(self):
        # Benchmark Label
        self.benchmark_label = tk.Label(self.root, text="Benchmark Algorithm:")
        self.benchmark_label.grid(row=11, column=0, padx=10, pady=10, sticky="w")

        # Benchmark Algorithm Dropdown
        self.benchmark_choices = ["AUTOLYKOS2", "BEAM-III", "C29AE", "C29D", "C29M", "C30CTX", "C31", "C32", "CR29-32", "CR29-40", "CR29-48", "EQUI144_5", "EQUI192_7", "EQUI210_9", "ETCHASH", "ETHASH", "ZEL"]
        self.benchmark_dropdown = ttk.Combobox(self.root, values=self.benchmark_choices)
        self.benchmark_dropdown.grid(row=11, column=1, padx=10, pady=10)

        # Benchmark Button
        self.benchmark_button = tk.Button(self.root, text="Run Benchmark", command=self.run_benchmark)
        self.benchmark_button.grid(row=11, column=2, columnspan=2, padx=10, pady=10)

    def create_stop_buttons(self):
        # Stop lolMiner Button
        self.stop_server_button = tk.Button(self.root, text="Stop lolMiner", command=self.stop_lolminer)
        self.stop_server_button.grid(row=12, column=0, columnspan=2, padx=10, pady=10)

        # Stop Benchmark Button
        self.stop_benchmark_button = tk.Button(self.root, text="Stop Benchmark", command=self.stop_benchmark)
        self.stop_benchmark_button.grid(row=12, column=2, columnspan=2, padx=10, pady=10)

    def run_lolminer(self):
        try:
            self.miner_process = subprocess.Popen(["mate-terminal", "--", "./lolMiner"], preexec_fn=os.setsid)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run lolMiner: {e}")

    def stop_lolminer(self):
        if hasattr(self, 'miner_process') and self.miner_process:
            try:
                os.killpg(os.getpgid(self.miner_process.pid), 9)  # Send kill signal to process group
                messagebox.showinfo("Info", "lolMiner stopped.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to stop lolMiner: {e}")
        else:
            messagebox.showwarning("Warning", "No lolMiner process is running.")

    def run_benchmark(self):
        try:
            algorithm = self.benchmark_dropdown.get()
            if not algorithm:
                messagebox.showwarning("Warning", "Please select an algorithm for benchmarking.")
                return

            self.benchmark_process = subprocess.Popen(["mate-terminal", "--", "./lolMiner", "--benchmark", algorithm], preexec_fn=os.setsid)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run benchmark: {e}")

    def stop_benchmark(self):
        if hasattr(self, 'benchmark_process') and self.benchmark_process:
            try:
                os.killpg(os.getpgid(self.benchmark_process.pid), 9)  # Send kill signal to process group
                messagebox.showinfo("Info", "Benchmark stopped.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to stop benchmark: {e}")
        else:
            messagebox.showwarning("Warning", "No benchmark process is running.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LolMinerGUI(root)
    root.mainloop()
