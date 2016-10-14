## drainage_density_plot.py
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## This function creates two subplots: of drainage density against CRN-derived erosion
## rate for two field sites.  The user needs to specify the OutputFigureName and
## OutputFigureFormat.  It takes two input text files, one for each field site.  They
## should have the following layout with 9 columns:
## drainage_density mean_slope slope_standard_deviation slope_standard_error 
## cosmogenic_erosion_rate cosmogenic_erosion_error drainage_area 
## mean_hilltop_curvature mean_hilltop_curvature_standard_error
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## FJC 21/01/14
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#import modules
import numpy as np, matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.cm as cmx
from scipy import stats
from mpl_toolkits.axes_grid1 import make_axes_locatable

def make_plots(DataDirectory, DEM_name):
    

    # Set up fonts for plots
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['arial']
    rcParams['font.size'] = 12
    
    #norm = mpl.colors.Normalize(vmin=0, vmax=6)
    
    ########################
    #                      #
    #   READ IN THE DATA   #
    #                      #
    ########################

    FileName = DEM_name+'_drainage_density_cosmo.txt'
    OutputFigureName = DEM_name+'_drainage_density_cosmo'
    OutputFigureFormat = 'png'
    f = open(DataDirectory + FileName,'r')  # open file
    lines = f.readlines()   # read in the data
    no_lines = len(lines)   # get the number of lines (=number of data)

    # data variables
    drainage_density = np.zeros(no_lines)        # drainage density
    mean_slope = np.zeros(no_lines)              # mean slope
    slope_stdev = np.zeros(no_lines)             # standard deviation of slope
    slope_sterr = np.zeros(no_lines)             # standard error of slope
    erosion_rate = np.zeros(no_lines)            # cosmo erosion rate
    cosmo_error = np.zeros(no_lines)             # error on cosmo dates
    drainage_area = np.zeros(no_lines)           # drainage area
    mean_cht = np.zeros(no_lines)                # mean hilltop curvature
    cht_sterr = np.zeros(no_lines)               # standard error of curvature

  
    for i in range (0,no_lines):
        line = lines[i].strip().split(" ")
        #print line
        drainage_density[i] = float(line[0])
        mean_slope[i] = float(line[1])
        slope_stdev[i] = float(line[2])
        slope_sterr[i] = float(line[3])
        erosion_rate[i] = float(line[4])
        cosmo_error[i] = float(line[5])
        drainage_area[i] = float(line[6])/1000000
        mean_cht[i] = float(line[7])
        cht_sterr[i] = float(line[8])
        
    f.close()    
    
    #############################    
    #                           #
    #       DO SOME STATS       #
    #                           #
    #############################
    
    erosion_rate = erosion_rate*10**-3
    cosmo_error = cosmo_error*10**-3
    
    drainage_density_log = log10(drainage_density)
    erosion_rate_log = log10(erosion_rate)
    
    gradient, intercept, r_value, p_value, st_err = stats.linregress(erosion_rate_log, drainage_density_log)
    print "Power law regression stats (erosion/drainage density) for ", FileName
    print "Gradient:", gradient
    print "P value:", p_value
    print "R2:", r_value
    print "Standard error", st_err
    
    x = np.linspace(0, np.max(erosion_rate)+0.1, 1000)
    
    intercept = 10**intercept
    y = intercept*x**gradient
    print "Intercept:", intercept
   
    
    ########################    
    #                      #
    #   MAKE SCATTERPLOTS  #
    #                      #
    ########################
    
    fig = plt.figure(1, facecolor='white', figsize=(6,5))
    
    ax = fig.add_subplot(111)    
    plt.errorbar(erosion_rate, drainage_density, xerr=cosmo_error, fmt='ko', lw = 1, alpha = 1, markersize=0, zorder=1)
    plt.scatter(erosion_rate, drainage_density, c=drainage_area, cmap=cmx.Reds, lw = 1, s=50, alpha = 1, label = 'Basin drainage area', zorder=2)
    sm = plt.cm.ScalarMappable(cmap=cmx.Reds,norm=plt.Normalize(vmin=0, vmax=np.max(drainage_area)))
    sm._A = []
    plt.plot(x,y, 'k--')
    plt.ylabel('Drainage density (m/m$^2$)')
    plt.xlabel('Erosion rate (m/kyr)')
    plt.xlim(0, np.max(erosion_rate)+0.01)
    plt.ylim(0,np.max(drainage_density)+0.001)
    yticks = ax.yaxis.get_major_ticks()
    yticks[0].label1.set_visible(False)
       
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right',size='5%', pad=0.2)   
    cbar = fig.colorbar(sm, cax=cax)
    cbar.set_label('Basin drainage area (km$^2$)')

    plt.tight_layout(pad=2)
    plt.savefig(DataDirectory + OutputFigureName + '.' + OutputFigureFormat, format=OutputFigureFormat, dpi=300)
    plt.clf()
    
    
if __name__ == "__main__":
	
    # change this to the path to your DEM
    DataDirectory = 'C:\\vagrantboxes\\LSDTopoTools\\Topographic_projects\\Feather_River\\'
    # Name of the DEM WITHOUT FILE EXTENSION
    DEM_name = 'fr1m_nogaps'
    make_plots(DataDirectory, DEM_name)    

	