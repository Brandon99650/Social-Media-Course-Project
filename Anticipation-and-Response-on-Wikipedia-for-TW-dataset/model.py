import numpy as np
import os
from scipy.optimize import least_squares
import matplotlib.pyplot as plt
from tqdm import tqdm
import pandas as pd

def pred_before(theta, t, tpeak):
    return (theta[0] * np.exp((t-tpeak)/theta[1]) + theta[2])

def residual_before(theta, tlist, ys:np.ndarray):
    return pred_before(theta, tlist, ys.shape[0]*1.0) - ys


def pred_after(theta, t, tpeak):
    return (theta[0] * np.exp(-(t-tpeak)/theta[1]) + theta[2])

def residual_after(theta, tlist, peak, ys:np.ndarray):
    return pred_after(theta, tlist, peak) - ys


def fit_before(serise_data:np.ndarray):
    theta0 = np.random.randint(2, 10, size=3).astype(np.float32)
    #theta0 = np.append(theta0, np.random.uniform(0.0,1.0))
    tlist = np.array(list(i for i in range(serise_data.shape[0]))).astype(np.float32)
    res1 = least_squares(residual_before, theta0, args=(tlist, serise_data), bounds=(0,np.inf))
    return res1.x

def fit_after(serise_data:np.ndarray, peak):
    theta0 = np.random.randint(2, 10,size=3).astype(np.float32)
    #theta0 = np.append(theta0, np.random.uniform(0.0,1.0))
    tlist = np.array(list(i+peak for i in range(serise_data.shape[0]))).astype(np.float32)
    res1 = least_squares(residual_after, theta0, args=(tlist, peak, serise_data), bounds=(0,np.inf))
    return res1.x


def main(g):
    root = os.path.join("data","actual",g)
    csvfiles = []
    names = []
    for d,_,f in os.walk(root):
        for fi in f:
            if fi[-3:] == "csv":
                names.append(fi)
                csvfiles.append(os.path.join(d, fi))

    paras = {
        "title":[],
        #"c+":[], "c-":[],
        "a-":[],"b-":[],"tau-":[],
        "a+":[],"b+":[],"tau+":[]
    }
    save_root = os.path.join(f"data","fit",g)
    
    if not os.path.exists(save_root):
        os.mkdir(save_root)


    for file, fname in tqdm(zip(csvfiles, names), total=len(csvfiles)):
        
        if os.path.exists(
            os.path.join(save_root,f"{fname[:-4]}.npy")
        ):
            print(fname[:-4], "OK")
            pass
        serise_data = pd.read_csv(file)["views"].values.astype(np.float32)
        serise_data = serise_data/100
        peak = np.argmax(serise_data)
    
        serise_data_before = serise_data[:peak]
        tlist_before = np.array(list(i for i in range(serise_data_before.shape[0]))).astype(np.float32)
        th_before = fit_before(serise_data=serise_data_before)
        fit_y_before = pred_before(theta=th_before, t=tlist_before, tpeak=peak*1.0)

        serise_data_after = serise_data[peak:]
        tlist_after = np.array(list(i+peak for i in range(serise_data_after.shape[0]))).astype(np.float32)
        th_after = fit_after(serise_data=serise_data_after, peak=peak*1.0)
        fit_y_after = pred_after(theta=th_after, t=tlist_after, tpeak=peak*1.0)
        
        fit_y = np.concatenate((fit_y_before, fit_y_after))
        plt.figure(dpi=800)
        plt.plot(list(_ for _ in range(fit_y.shape[0])), serise_data, label="origin")
        plt.plot(list(_ for _ in range(fit_y.shape[0])), fit_y, label="fit")
        plt.legend()
        plt.savefig(os.path.join(save_root,f"{fname[:-4]}.jpg"))
        plt.close()

        np.save(os.path.join(save_root,fname[:-4]), fit_y)

        paras["title"].append(fname[:-4])
        
        paras["a-"].append(th_before[0])
        paras["tau-"].append(th_before[1])
        paras["b-"].append(th_before[2])
        #paras["c-"].append(th_before[3])

        paras["a+"].append(th_after[0])
        paras["tau+"].append(th_after[1])
        paras["b+"].append(th_after[2])
        #paras["c+"].append(th_after[3])


    result_df = pd.DataFrame(paras)
    """
    db=os.path.join(save_root,"paras.csv")
    if os.path.exists(db):
        pre_df = pd.read_csv(db)
    result_df = pd.concat((pre_df, result_df))
    """
    result_df.to_csv(os.path.join(save_root,"paras.csv"), index=False)

if __name__ == "__main__":
    
    main("91")
