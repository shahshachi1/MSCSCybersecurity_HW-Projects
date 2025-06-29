import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt
from keras.utils import to_categorical

# --------- Configuration ---------
SCENARIO = 2  # Set 1 (binary), 2 (multi-class), or 3 (attack group)

# --------- Attack Group Mapping ---------
ATTACK_MAP = {
    'back': 'DoS', 'land': 'DoS', 'neptune': 'DoS', 'pod': 'DoS', 'smurf': 'DoS',
    'teardrop': 'DoS', 'mailbomb': 'DoS', 'apache2': 'DoS', 'processtable': 'DoS',
    'udpstorm': 'DoS', 'ipsweep': 'Probe', 'nmap': 'Probe', 'portsweep': 'Probe',
    'satan': 'Probe', 'mscan': 'Probe', 'saint': 'Probe', 'ftp_write': 'R2L',
    'guess_passwd': 'R2L', 'imap': 'R2L', 'multihop': 'R2L', 'phf': 'R2L',
    'spy': 'R2L', 'warezclient': 'R2L', 'warezmaster': 'R2L', 'sendmail': 'R2L',
    'named': 'R2L', 'snmpgetattack': 'R2L', 'snmpguess': 'R2L', 'xlock': 'R2L',
    'xsnoop': 'R2L', 'worm': 'R2L', 'buffer_overflow': 'U2R', 'loadmodule': 'U2R',
    'perl': 'U2R', 'rootkit': 'U2R', 'httptunnel': 'U2R', 'ps': 'U2R', 'sqlattack': 'U2R',
    'xterm': 'U2R', 'normal': 'normal'
}

# --------- Preprocessors ---------
def preprocess(df, scenario):
    X = df.iloc[:, :-2].values
    y_raw = df.iloc[:, -2].values
    if scenario == 1:
        y_raw = np.array(['normal' if label == 'normal' else 'attack' for label in y_raw])
        y = y_raw  # ✅ FIXED: Assign y
    elif scenario == 2:
        y = y_raw
    elif scenario == 3:
        y = np.array([ATTACK_MAP.get(label, 'normal') for label in y_raw])
    else:
        raise ValueError("Invalid scenario")
    ct = ColumnTransformer([('encoder', OneHotEncoder(handle_unknown='ignore'), [1,2,3])], remainder='passthrough')
    X = np.array(ct.fit_transform(X), dtype=np.float32)
    le = LabelEncoder()
    y = le.fit_transform(y)
    return X, y, ct, le

def transform_with_preprocessor(df, ct, le, scenario):
    X = df.iloc[:, :-2].values
    y_raw = df.iloc[:, -2].values
    if scenario == 1:
        y_raw = np.array(['normal' if label == 'normal' else 'attack' for label in y_raw])
    elif scenario == 3:
        y_raw = np.array([ATTACK_MAP.get(label, 'normal') for label in y_raw])
    # Filter to known labels
    known_mask = np.isin(y_raw, le.classes_)
    X = X[known_mask]
    y_raw = y_raw[known_mask]
    if len(X) == 0:
        raise ValueError(f"No known labels in test set for scenario {scenario}")
    y = le.transform(y_raw)
    X = np.array(ct.transform(X), dtype=np.float32)
    print(f"[{scenario}] X_test shape: {X.shape}")
    print(f"[{scenario}] y_test shape: {y.shape}")
    return X, y

def run_scenario(SCENARIO):
    print(f"\n===== Running Scenario {SCENARIO} =====")

    # Load and preprocess
    train_df = pd.read_csv('train_SA.csv')
    test_df = pd.read_csv('test_SA.csv')
    X_train, y_train, ct, le = preprocess(train_df, SCENARIO)
    X_test, y_test = transform_with_preprocessor(test_df, ct, le, SCENARIO)

    print("X_train shape:", X_train.shape)
    print("X_test shape:", X_test.shape)

    # Normalize
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    # Encode Y
    if SCENARIO != 1:
        y_train = to_categorical(y_train)
        y_test = to_categorical(y_test)
        output_units = y_train.shape[1]
        loss_fn = 'categorical_crossentropy'
        final_activation = 'softmax'
    else:
        output_units = 1
        loss_fn = 'binary_crossentropy'
        final_activation = 'sigmoid'

    # Model
    model = Sequential()
    model.add(Dense(64, activation='relu', input_dim=X_train.shape[1]))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(output_units, activation=final_activation))
    model.compile(optimizer='adam', loss=loss_fn, metrics=['accuracy'])

    # Train
    history = model.fit(X_train, y_train, validation_split=0.2, epochs=10, batch_size=32, verbose=1)

    # Evaluate
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"\nScenario {SCENARIO} Test Loss: {loss:.4f}")
    print(f"Scenario {SCENARIO} Test Accuracy: {accuracy * 100:.2f}%")

    # Plot Accuracy
    acc_key = 'accuracy' if 'accuracy' in history.history else 'acc'
    val_acc_key = 'val_accuracy' if 'val_accuracy' in history.history else 'val_acc'
    plt.plot(history.history[acc_key], label='Train Accuracy')
    plt.plot(history.history[val_acc_key], label='Val Accuracy')
    plt.title(f'Scenario {SCENARIO} Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.grid()
    plt.savefig(f"accuracy_plot_scenario_{SCENARIO}.png")
    plt.show()

    # Plot Loss
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Val Loss')
    plt.title(f'Scenario {SCENARIO} Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid()
    plt.savefig(f"loss_plot_scenario_{SCENARIO}.png")
    plt.show()


# Run all scenarios
for scenario in [1, 2, 3]:
    run_scenario(scenario)

