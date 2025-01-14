import tkinter as tk
from tkinter import ttk, filedialog
import subprocess
import json
import threading

class LolMinerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("lolMiner GUI")
        self.settings = {}
        self.mining_entries = {}
        self.management_entries = {}
        self.statistics_entries = {}
        self.overclock_entries = {}
        self.ethash_entries = {}
        self.altcoin_entries = {}
        self.ethash_expert_entries = {}
        self.algorithm_split_entries = {}
        self.process = None

        # Notebook for tabs
        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True)

        # Add tabs
        self.add_tab(notebook, "Mining", self.mining_entries, self.mining_options())
        self.add_tab(notebook, "Management", self.management_entries, self.management_options())
        self.add_tab(notebook, "API", self.statistics_entries, self.statistics_options())
        self.add_tab(notebook, "Overclock", self.overclock_entries, self.overclock_options())
        self.add_tab(notebook, "Ethash", self.ethash_entries, self.ethash_options())
        self.add_tab(notebook, "Altcoin", self.altcoin_entries, self.altcoin_options())
        self.add_tab(notebook, "Ethash Expert", self.ethash_expert_entries, self.ethash_expert_options())
        self.add_tab(notebook, "Algorithm Split", self.algorithm_split_entries, self.algorithm_split_options())

        # Debug tab
        self.debug_text = tk.Text(root, state="disabled", height=20, wrap="none")
        notebook.add(self.debug_text, text="Debug")

        # Control buttons
        buttons_frame = tk.Frame(root)
        buttons_frame.pack(fill="x", pady=10)

        tk.Button(buttons_frame, text="Save", command=self.save_settings).pack(side="left", padx=5)
        tk.Button(buttons_frame, text="Load", command=self.load_settings).pack(side="left", padx=5)
        tk.Button(buttons_frame, text="Run lolMiner", command=self.run_lolminer).pack(side="left", padx=5)
        tk.Button(buttons_frame, text="Benchmark", command=self.run_benchmark).pack(side="left", padx=5)
        tk.Button(buttons_frame, text="Stop", command=self.stop_lolminer).pack(side="left", padx=5)

    def add_tab(self, notebook, tab_name, entries, options):
        """Add a tab with options."""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text=tab_name)
        self.add_options(tab, entries, options)

    def add_options(self, tab, entries, options):
        """Add options to a given tab."""
        for row, (label_text, param, key, *widget_type) in enumerate(options):
            tk.Label(tab, text=label_text).grid(row=row, column=0, sticky="w", padx=5, pady=2)
            if widget_type and widget_type[0] == "checkbox":
                var = tk.IntVar(value=0)  # Ensure all checkboxes are unchecked initially
                checkbox = tk.Checkbutton(tab, variable=var)
                checkbox.grid(row=row, column=1, sticky="w", padx=5, pady=2)
                entries[key] = var
            elif widget_type and widget_type[0] == "dropdown":
                choices = widget_type[1]
                combobox = ttk.Combobox(tab, values=choices, state="readonly", width=37)
                combobox.grid(row=row, column=1, padx=5, pady=2)
                entries[key] = combobox
            else:
                entry = tk.Entry(tab, width=40)
                default_value = widget_type[0] if widget_type else ""  # Set default value if provided
                entry.insert(0, default_value)
                entry.grid(row=row, column=1, padx=5, pady=2)
                entries[key] = entry

    def save_settings(self):
        """Save settings to a file."""
        self.settings = {
            key: entry.get() if isinstance(entry, (tk.Entry, ttk.Combobox)) else entry.get()
            for key, entry in {
                **self.mining_entries,
                **self.management_entries,
                **self.statistics_entries,
                **self.overclock_entries,
                **self.ethash_entries,
                **self.altcoin_entries,
                **self.ethash_expert_entries,
                **self.algorithm_split_entries,
            }.items()
        }
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if file_path:
            with open(file_path, "w") as f:
                json.dump(self.settings, f, indent=4)

    def load_settings(self):
        """Load settings from a file."""
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            try:
                with open(file_path, "r") as f:
                    self.settings = json.load(f)
                self.update_ui_with_settings()
            except FileNotFoundError:
                pass  # Fail silently if no settings file is found

    def update_ui_with_settings(self):
        """Update the UI with loaded settings."""
        for tab_entries in [
            self.mining_entries,
            self.management_entries,
            self.statistics_entries,
            self.overclock_entries,
            self.ethash_entries,
            self.altcoin_entries,
            self.ethash_expert_entries,
            self.algorithm_split_entries,
        ]:
            for key, widget in tab_entries.items():
                value = self.settings.get(key, "")
                if isinstance(widget, tk.Entry):
                    widget.delete(0, tk.END)
                    widget.insert(0, value)
                elif isinstance(widget, ttk.Combobox):
                    widget.set(value)

    def append_debug_message(self, message):
        """Append a message to the debug window."""
        self.debug_text.configure(state="normal")
        self.debug_text.insert(tk.END, message + "\n")
        self.debug_text.configure(state="disabled")
        self.debug_text.see(tk.END)

    def run_lolminer(self):
        """Run lolMiner with current settings."""
        if self.process:
            self.append_debug_message("lolMiner is already running.")
            return

        command = ["./lolMiner", "--nocolor"]

        # Collect settings and add to command
        for key, widget in {
            **self.mining_entries,
            **self.management_entries,
            **self.statistics_entries,
            **self.overclock_entries,
            **self.ethash_entries,
            **self.altcoin_entries,
            **self.ethash_expert_entries,
            **self.algorithm_split_entries,
        }.items():
            value = widget.get() if isinstance(widget, (tk.Entry, ttk.Combobox)) else widget.get()

            if value:  # For all widget types
                command.append(f"--{key}={value}")

        def run():
            self.append_debug_message("Starting lolMiner...")
            try:
                self.process = subprocess.Popen(
                    command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )

                for line in self.process.stdout:
                    self.append_debug_message(line.strip())
                for line in self.process.stderr:
                    self.append_debug_message(line.strip())
            except Exception as e:
                self.append_debug_message(f"Error running lolMiner: {e}")
            finally:
                self.process = None
                self.append_debug_message("lolMiner has stopped.")

        threading.Thread(target=run, daemon=True).start()

    def stop_lolminer(self):
        """Stop the running lolMiner process."""
        if self.process:
            self.process.terminate()
            self.process = None
            self.append_debug_message("lolMiner process terminated.")
        else:
            self.append_debug_message("No lolMiner process is running.")

    def run_benchmark(self):
        """Run benchmark for selected algorithm."""
        benchmark_command = ["./lolMiner", "--nocolor", "--benchmark"]

        # Collect benchmark settings
        algo = self.mining_entries.get("algo")
        if algo and algo.get():
            benchmark_command.append(algo.get())

        def run():
            self.append_debug_message("Starting benchmark...")
            try:
                process = subprocess.Popen(
                    benchmark_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )

                for line in process.stdout:
                    self.append_debug_message(line.strip())
                for line in process.stderr:
                    self.append_debug_message(line.strip())
            except Exception as e:
                self.append_debug_message(f"Error during benchmark: {e}")
            finally:
                self.append_debug_message("Benchmark has completed.")

        threading.Thread(target=run, daemon=True).start()

    def kill_all_lolminer(self):
        """Forcefully kill all lolMiner processes."""
        try:
            subprocess.run(["killall", "-9", "lolMiner"], check=True)
            self.append_debug_message("All lolMiner processes have been forcefully terminated.")
        except subprocess.CalledProcessError:
            self.append_debug_message("Failed to kill lolMiner processes. They may not be running.")

    @staticmethod
    def mining_options():
        algorithms = [
            "", "AUTOLYKOS2", "BEAM-III", "C29AE", "C29D", "C29M", "C30CTX", "C31", "C32", "CR29-32", "CR29-40", "CR29-48",
            "EQUI144_5", "EQUI192_7", "EQUI210_9", "ETCHASH", "ETHASH", "ZEL"
        ]
        return [
            ("Algorithm", "-a", "algo", "dropdown", algorithms),
            ("Pool", "-p", "pool", "stratum+tcp://etchash.auto.nicehash.com:9200"),
            ("Wallet", "-u", "user", "38bj4uu8uDsnC5NjoeGb8TMviBCEtMiaet"),
            ("Password", "--pass", "pass"),
            ("TLS", "--tls", "tls", "checkbox"),
            ("Devices", "--devices", "devices"),
        ]

    @staticmethod
    def management_options():
        return [
            ("Watchdog", "--watchdog", "watchdog"),
            ("Temp Start", "--tstart", "tstart"),
            ("Temp Stop", "--tstop", "tstop"),
        ]

    @staticmethod
    def statistics_options():
        return [
            ("API Port", "--apiport", "apiport"),
            ("API Host", "--apihost", "apihost", "0.0.0.0"),
            ("Long Stats", "--longstats", "longstats"),
            ("Short Stats", "--shortstats", "shortstats"),
        ]

    @staticmethod
    def overclock_options():
        return [
            ("Core Clock", "--cclk", "cclk"),
            ("Memory Clock", "--mclk", "mclk"),
            ("Core Offset", "--coff", "coff"),
            ("Memory Offset", "--moff", "moff"),
            ("Fan Speed", "--fan", "fan"),
            ("Power Limit", "--pl", "pl"),
            ("Disable OC Reset", "--no-oc-reset", "no-oc-reset", "checkbox"),
        ]

    @staticmethod
    def ethash_options():
        return [
            ("Ethash Stratum", "--ethstratum", "ethstratum", "ETHPROXY"),
            ("Worker", "--worker", "worker", "eth1.0"),
        ]

    @staticmethod
    def altcoin_options():
        coins = [
            "", "AION", "AUTO144_5", "AUTO192_7", "BEAM", "BTCZ", "BTG", "ETC", "ETH", "CTXC", "EXCC",
            "GRIN-C29M", "GRIN-C32", "MWC-C29D", "MWC-C31", "XSG", "YEC", "ZCL", "ZEL", "ZER"
        ]
        return [
            ("Coin", "--coin", "coin", "dropdown", coins),
        ]

    @staticmethod
    def ethash_expert_options():
        return [
            ("Work Multi", "--workmulti", "workmulti"),
            ("Rebuild Defect", "--rebuild-defect", "rebuild-defect"),
        ]

    @staticmethod
    def algorithm_split_options():
        return [
            ("Dual Mode", "--dualmode", "dualmode", "none"),
            ("Dual Pool", "--dualpool", "dualpool"),
            ("Dual User", "--dualuser", "dualuser"),
            ("Dual Password", "--dualpass", "dualpass"),
            ("Dual Worker", "--dualworker", "dualworker", "eth1.0"),
            ("Dual TLS", "--dualtls", "dualtls", "checkbox"),
            ("Dual Devices", "--dualdevices", "dualdevices"),
            ("Dual Factor", "--dualfactor", "dualfactor", "auto"),
            ("Max Dual Impact", "--maxdualimpact", "maxdualimpact", "auto"),
        ]

if __name__ == "__main__":
    root = tk.Tk()
    app = LolMinerGUI(root)
    root.mainloop()
