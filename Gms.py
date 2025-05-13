import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.dates import DateFormatter
from matplotlib import dates as mdates

def prepare_data(file_path):
    df = pd.read_csv(file_path)
    df = df.copy()
    # Convert 'Lista' in MM-YY format to datetime
    df['Lista'] = pd.to_datetime(df['Lista'], format='%m/%y')
    df['Rating'] = df['Rating'].astype(float)
    return df[['Lista', 'Rating']].sort_values('Lista')

def create_multi_stock_animation():
    # Load and prepare all player data
    players = {
        'Mequinho': prepare_data(r"C:\repositorios\GMs_BR\Meckinho.csv"),
        'Sunye': prepare_data(r"C:\repositorios\GMs_BR\Sunye.csv"),
        'Milos': prepare_data(r"C:\repositorios\GMs_BR\Milos.csv"),
        'Lima': prepare_data(r"C:\repositorios\GMs_BR\Lima.csv"),
        'Matsuura': prepare_data(r"C:\repositorios\GMs_BR\Matsuura.csv"),
        'Vescovi': prepare_data(r"C:\repositorios\GMs_BR\Vescovi.csv"),
        'Leitao': prepare_data(r"C:\repositorios\GMs_BR\Leitao.csv"),
        'El_Debs': prepare_data(r"C:\repositorios\GMs_BR\El_Debs.csv"),
        'Krikor': prepare_data(r"C:\repositorios\GMs_BR\Krikor.csv"),
        'Diamant': prepare_data(r"C:\repositorios\GMs_BR\Diamant.csv"),
        'Fier': prepare_data(r"C:\repositorios\GMs_BR\Fier.csv"),
        'Barbosa': prepare_data(r"C:\repositorios\GMs_BR\Barbosa.csv"),
        'Yago': prepare_data(r"C:\repositorios\GMs_BR\Yago.csv"),
        'Supi': prepare_data(r"C:\repositorios\GMs_BR\Supi.csv"),
        'Quintiliano': prepare_data(r"C:\repositorios\GMs_BR\Quinti.csv")
    }

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Set date range
    start_date = pd.to_datetime("01/71", format="%m/%y")  # Jan 1971
    end_date = pd.to_datetime("05/25", format="%m/%y")    # May 2025
    ax.set_xlim(start_date, end_date)
    
    ax.set_ylim(2300, 2700)  # Fixed range for chess ratings

    ax.xaxis.set_major_formatter(DateFormatter('%Y'))  # "1971", "1972", ..., "2025"
    plt.xticks(rotation=45)  # Rotate for readability

    # Optional: Show major ticks every 5 years
    ax.xaxis.set_major_locator(mdates.YearLocator(5)) 

    # Color palette
    colors = {
        'Mequinho': '#ED1C24',
        'Sunye': '#76B900',
        'Milos': '#0071C5',
        'Lima': '#9400D3',
        'Matsuura': '#FFD700',
        'Vescovi': '#008080',
        'Leitao': '#FF1493',
        'El_Debs': '#FF7F50',
        'Krikor': '#6A5ACD',
        'Diamant': '#32CD32',
        'Fier': '#008B8B',
        'Barbosa': '#DC143C',
        'Yago': '#4682B4',
        'Supi': '#DA70D6',
        'Quintiliano': '#F4A460'
    }
    
    # Create lines and text objects
    lines = {}
    texts = {}
    for name, color in colors.items():
        lines[name], = ax.plot([], [], lw=2, color=color, label=name)
        texts[name] = ax.text(0, 0, '', color='white' if color != '#FFD700' else 'black',
                             fontweight='bold', bbox=dict(facecolor=color, alpha=0.7, edgecolor='none', pad=3))
    
    # Animation functions
    def init():
        for line in lines.values():
            line.set_data([], [])
        for text in texts.values():
            text.set_text('')
        return list(lines.values()) + list(texts.values())
    
    def animate(frame):
        artists = []
        current_date = start_date + pd.DateOffset(months=frame)

        for name, player in players.items():
            x = player['Lista'].iloc[:frame]
            y = player['Rating'].iloc[:frame]
            lines[name].set_data(x, y)
            artists.append(lines[name])
            
            if len(y) > 0:
                texts[name].set_position((x.iloc[-1], y.iloc[-1]))
                texts[name].set_text(f'{name}: {y.iloc[-1]:.0f}')
                artists.append(texts[name])
        
        return artists
    
    # Animation settings
    max_frames = max(len(p) for p in players.values())
    anim = animation.FuncAnimation(
        fig, animate, frames=max_frames,
        init_func=init, interval=300, blit=True
    )
    
    # Plot formatting
    ax.legend(loc='upper left')
    ax.set_title('Evolução dos 15 GMs Brasileiros', pad=15)
    ax.set_xlabel('Date')
    ax.set_ylabel('Rating')
    ax.xaxis.set_major_formatter(DateFormatter('%y-%m'))
    plt.xticks(rotation=45)
    ax.grid(True, linestyle='--', alpha=0.7)
    plt.subplots_adjust(bottom=0.2)
    
    return anim, fig

# Create and show animation
anim, fig = create_multi_stock_animation()
plt.show()

# To save:
# anim.save('chess_gms.mp4', writer='ffmpeg', fps=30)
# anim.save('chess_gms.gif', writer='imagemagick', fps=30)