function run_test_single_model
% Copyright (c) 2014-present University of Illinois at Urbana-Champaign
% All rights reserved.
% 		
% Developed by:     Po-Sen Huang, Paris Smaragdis
%                   Department of Electrical and Computer Engineering
%                   Department of Computer Science
%
% Given a model, evaluate the performance.
    basedir = '../../../';
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
        
    
    dialects = {'DR1', 'DR2', 'DR3', 'DR4', 'DR5', 'DR6', 'DR7'};

    % Load model
    load([ModelPath, filesep, 'denoising_model_', num2str(j),'.mat']);
    %%
    savedir = {basedir, 'codes', '/', 'denoising', '/', 'denoised_set'};

    for i=1:length(dialects)
	dialect = dialects{i};
        dataset = {basedir, 'codes', '/', 'denoising', '/', 'Data', '/', 'TIMIT', '/', 'TEST', '/', char(dialect)};
        dataset_arr = dir(strrep(strjoin(dataset), ' ', ''))'; 
	for j=1:length(dataset_arr)
            speaker = dataset_arr(j);
	    dataset{13} = char('/');
            dataset{14} = speaker.name;
	    dataset{15} = char('/');
	    dataset{16} = char('*.WAV');
	    file_arr = dir(strrep(strjoin(dataset), ' ', ''))';
	    for k=1:length(file_arr)
		file = file_arr(k);
                dataset{15} = char('/');
                dataset{16} = file.name;
                disp(strrep(strjoin(dataset), ' ', ''));

	%{
		eI.saveDir = [baseDir, filesep, 'codes', filesep, 'denoising', ...
        filesep, 'demo', filesep, '', filesep];
    
	    
	index = 2;
	[speech, fs] = audioread(['wav', filesep, 'original_speech', num2str(index), '.wav']);
	[noise, fs] = audioread(['wav', filesep, 'original_noise',num2str(index),'.wav']);
	    
	r = snr(speech, noise);
	factor = 10^((3-r)/20);

	r = snr(speech, noise / factor);
	disp(r);
	 
	x = speech + noise;    
	eI.fs = fs;
	  
	audiowrite([eI.saveDir, filesep, 'noisy_speech', '.wav'], x, fs);
	    
	%%
	output = test_denoising_general_kl_bss3(x', theta, eI, 'testall', 0);
	%%
	sz = 1024.*[1 1/4];
	wn = sqrt( hann( sz(1), 'periodic')); % hann window
	wav_signal = stft2( output.source_signal, sz(1), sz(2), 0, wn);
	wav_noise = stft2( output.source_noise, sz(1), sz(2), 0, wn);
	wav_signal = wav_signal./max(abs(wav_signal));
	wav_noise = wav_noise./max(abs(wav_noise));    

	audiowrite([eI.saveDir, filesep,'separated_speech',num2str(index),'.wav'], wav_signal, fs);
	% audiowrite([eI.saveDir, filesep,'separated_noise',num2str(index),'.wav'], wav_noise, fs);
  %}	
            end
        end
    end
end
