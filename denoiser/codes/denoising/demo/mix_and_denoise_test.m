function run_test_single_model
% Copyright (c) 2014-present University of Illinois at Urbana-Champaign
% All rights reserved.
% 		
% Developed by:     Po-Sen Huang, Paris Smaragdis
%                   Department of Electrical and Computer Engineering
%                   Department of Computer Science
%
% Given a model, evaluate the performance.
    warning('off', 'MATLAB:MKDIR:DirectoryExists');
    basedir = '../../../';
    base_save = '../../../../';
    addpath([basedir, filesep, 'codes']);
    addpath([basedir, filesep, 'codes', filesep, 'denoising']);

    addpath([basedir, filesep, 'tools', filesep,'bss_eval']);
    addpath([basedir, filesep, 'tools', filesep,'bss_eval_3']);
    addpath([basedir, filesep, 'tools', filesep,'labrosa']);

    ModelPath=[basedir, filesep, 'codes',filesep,'denoising', filesep, 'demo'];
    
    global SDR;
    global SDR_bss3;

    SDR.deviter=0;   SDR.devmax=0;   SDR.testmax=0;
    SDR.devsar=0; SDR.devsir=0; SDR.testsar=0; SDR.testsir=0;
    SDR_bss3.deviter=0;   SDR_bss3.devmax=0;   SDR_bss3.testmax=0;
    SDR_bss3.devsar=0; SDR_bss3.devsir=0; SDR_bss3.testsar=0; SDR_bss3.testsir=0;

    j=870;
        
    
    dialects = {'DR1', 'DR2', 'DR3', 'DR4', 'DR5', 'DR6', 'DR7', 'DR8'}; 
    ratios = [-20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30];
    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    
    % Load model
    load([ModelPath, filesep, 'denoising_model_', num2str(j),'.mat']);
    %%
    for num=nums
        for ratio=ratios
            for i=1:length(dialects)
                dialect = dialects{i};
                dataset = {basedir, 'codes', '/', 'denoising', '/', 'Data', '/', 'TIMIT', '/', 'TEST', '/', char(dialect)};
                dataset_arr = dir(strrep(strjoin(dataset), ' ', ''))'; 
                for j=3:length(dataset_arr)
                    dataset = {basedir, 'codes', '/', 'denoising', '/', 'Data', '/', 'TIMIT', '/', 'TEST', '/', char(dialect)};
                    speaker = dataset_arr(j);
                    dataset{13} = char('/');
                    dataset{14} = speaker.name;
                    save_dir = {base_save, 'las', '/', 'noised_data', '/', num2str(num), '/', 'TIMIT', '/', 'TEST', '/', char(dialect), '/', speaker.name};
                    %save_dir = {base_save, 'las', '/', 'denoised_data', '/', num2str(num), '/', 'TIMIT', '/', 'TEST', '/', char(dialect), '/', speaker.name};
                    save_dir{8} = char(['TIMIT_noisy' '_' num2str(ratio)]);
                    %save_dir{8} = char(['TIMIT_denoised' '_' num2str(ratio)]);

                    mkdir(strrep(strjoin(save_dir), ' ', ''));

                    dataset{15} = char('/');
                    dataset{16} = char('*.wav');
                    file_arr = dir(strrep(strjoin(dataset), ' ', ''))';

                    for k=1:length(file_arr)
                    file = file_arr(k);
                    dataset{15} = char('/');
                    dataset{16} = file.name;
                    file_path = strrep(strjoin(dataset), ' ', '');

                    save_dir{15} = char('/');
                    save_dir{16} = file.name;
                    save_path = strrep(strjoin(save_dir), ' ', '');

                    phn_path = [char(file_path(1:length(file_path)-3)), char('PHN')];
                    phn_save_path = [char(save_path(1:length(save_path)-3)), char('PHN')];
                    copyfile(phn_path, phn_save_path)

                    noise_dir = {basedir, 'codes', '/', 'denoising', '/', 'Data', '/', 'noise'};
                    noise_arr = dir(strrep(strjoin(noise_dir), ' ', ''));
                    len = cast(length(noise_arr), 'uint8');
                    n = randi([3, len]);

                    noise_dir{9} = char('/');
                    noise_dir{10} = noise_arr(n).name;
                    noise_path = strrep(strjoin(noise_dir), ' ', '');

                    %%
                    [noise, fs] = audioread(noise_path);
                    [speech, fs] = audioread(file_path);
                    
                    noise = noise(1:length(speech));

                    r = snr(speech, noise);
                    factor = 10^((ratio-r)/20);

                    %% r = snr(speech, noise / factor);
                    %% disp(r);

                    x = speech + noise / factor;    
                    eI.fs = fs;

                    
 
                    sz = 1024.*[1 1/4];
                    wn = sqrt( hann( sz(1), 'periodic')); % hann window

                    % generate denoised
                    % output = test_denoising_general_kl_bss3(x', theta, eI, 'testall', 0);
                    % wav_signal = stft2( output.source_signal, sz(1), sz(2), 0, wn);
                    % wav_noise = stft2( output.source_noise, sz(1), sz(2), 0, wn);
                    % wav_signal = wav_signal./max(abs(wav_signal));
                    % wav_noise = wav_noise./max(abs(wav_noise));    
                    % audiowrite(save_path, wav_signal, fs)

                    %generate noisy voice 
                    audiowrite(save_path, x, fs)
                    end
                end
            disp(ratio)
            end
	    end
	end
end
