import datetime
from numpy import mean
import torch
import matplotlib.pyplot as plt
import os
import glob
import yaml
from torchviz import make_dot


def SaveModel(model,idx_epoch,optimizer,training_loader,testing_loader,epoch_train_losses,epoch_test_losses,folder_path,device,modelname,cnn_model_name,epochs,batch_size_val,val_loss,test_loss,model_evaluation,data_loaded,summarize):
    model.to('cpu')
    torch.save({
        'epoch': idx_epoch,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'loader_train': training_loader,
        'loader_test': testing_loader,
        'train_losses': epoch_train_losses,
        'test_losses': epoch_test_losses,
        }, folder_path + f'/{modelname}.pkl')
    model.to(device)
    if summarize:
        x = torch.randn(10,3,320,160).to(device)
        dot = make_dot(model(x), params=dict(model.named_parameters()))
        dot.format = 'pdf'
        dot.render(f'{folder_path}/{modelname}', view=False)

    # Save info
    current_date = datetime.datetime.now().strftime("%d-%m-%Y-%H:%M:%S")
    info_data = dict(
        model = dict(
            name = modelname,
            developer = os.getenv('automec_developer'),
            date = current_date,
            ml_arch = {"name":cnn_model_name, "epochs":epochs, 
                       "batch_size_val":batch_size_val,
                       "val_loss":val_loss, "tes_loss":test_loss},
            model_eval = model_evaluation,
            #comments = ml_comments
        ),
        dataset = data_loaded['dataset']
    )
    with open(f'{folder_path}/{modelname}.yaml', 'w') as outfile: #info
        yaml.dump(info_data, outfile, default_flow_style=False, sort_keys=False)


def LoadModel(model_path,model,device):
    checkpoint = torch.load(model_path)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.to(device) # move the model variable to the gpu if one exists
    return model

def SaveGraph(train_losses,test_losses,folder_name):
    plt.figure()
    plt.plot(train_losses, label='train loss')
    plt.plot(test_losses, label='test loss')
    plt.xlabel("Epoch")    
    plt.ylabel("Loss")   
    plt.legend()
    plt.savefig(f'{folder_name}/losses.png')