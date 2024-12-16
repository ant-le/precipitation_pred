import matplotlib.pyplot as plt


def seasonal_trends(df, agg_func:str):
    fig, axs = plt.subplot_mosaic('012;333', figsize=(12,6), tight_layout=True)
    fig.supylabel('{} Precipitation'.format(agg_func.capitalize()))
    fig.suptitle("Time-Related Trends by {} for Target Variable".format(agg_func.capitalize()))
    for idx in axs:
        if int(idx) < 3:
            aggregated_data = df.prec.groupby(level=int(idx)).agg(agg_func.lower()) 
            axs[idx].set_xlabel(df.index.names[int(idx)].capitalize())
        else:
            aggregated_data = df.groupby('DOY')['prec'].agg(agg_func)
            axs[idx].set_xlabel('Day of Year')
                                
        axs[idx].bar(
            aggregated_data.index,
            aggregated_data,
            width=.6
        )
        axs[idx].plot(
            aggregated_data.index,
            aggregated_data,
            c='gray',
        )
        axs[idx].grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
    plt.show()


def regional_trends(df, agg_func:str):
    grouped = df.groupby(level=(0, 3))['prec'].agg(agg_func.lower()).reset_index()
    boxplot_data = [grouped.loc[grouped['region'] == val, 'prec'].values
                    for val in grouped['region'].unique()]

    plt.figure(figsize=(15, 6))
    plt.boxplot(boxplot_data, labels=grouped['region'].unique(), patch_artist=True)

    plt.title('Region-related Trends for Target Variable')
    plt.xlabel('Region')
    plt.ylabel(f'{agg_func.capitalize()} Precipitation per Year')
    plt.xticks(rotation=45, fontsize=8)  
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()
