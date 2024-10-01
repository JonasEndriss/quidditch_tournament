from tqdm import tqdm

class TqdmTk(tqdm):
    def __init__(self, *args, **kwargs):
        self.tk_progress_bar = kwargs.pop('tk_progress_bar', None)
        super().__init__(*args, **kwargs)

    def update(self, n=1):
        super().update(n)
        if self.tk_progress_bar:
            self.tk_progress_bar['value'] = self.n
            self.tk_progress_bar.update_idletasks()