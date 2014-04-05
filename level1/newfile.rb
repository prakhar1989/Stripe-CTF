#!/usr/bin/env ruby
####MINER POWER LEVEL 5000!!!!!!!

require 'digest/sha1'

params = ["", "user-jpgjctdq"]

def prepare_index   
    params = ["lvl1-sojzq8kw@stripe-ctf.com:level1", "user-jpgjctdq"]
    text = File.read('LEDGER.txt')
      
        File.open('LEDGER.txt', 'a+') { |f| f.write("#{params[1]}: 1\n") }
    
    `git add LEDGER.txt`
end

def solve 
    # Brute force until you find something that's lexicographically
    # small than $difficulty.
    difficulty= File.read('difficulty.txt')[0..-2]
    puts "difficulty : #{difficulty}"
    # Create a Git tree object reflecting our current working
    # directory
    tree=`git write-tree`[0..-2]
    parent=`git rev-parse HEAD`[0..-2]
    timestamp= `date +%s`[0..-2]

    counter=0

     while counter=counter+1 do
        

        body="tree #{tree}
parent #{parent}
author Dushyant Rao <dushyant.rao@example.com> #{timestamp} +0000
committer Dushyant Rao <dushyant.rao@example.com> #{timestamp} +0000

Give me a Gitcoin:#{counter}"

        header = "commit #{body.length}\0"
        store = header + body

        # See http://git-scm.com/book/en/Git-Internals-Git-Objects for
        # details on Git objects.

        # sha1=`git hash-object -t commit --stdin <<< "#{body}"`
        sha1 = Digest::SHA1.hexdigest(store)
        # puts "Hash Number : #{counter} With SHA : #{sha1}"
        
        if  sha1[0..7] < difficulty  then
            # puts body
            File.open('body.txt', 'w') { |file| file.write(body) }
            puts "Mined a Gitcoin with commit: #{sha1}  at hash number #{counter}"
            `git hash-object -t commit -w body.txt  > /dev/null`
            `git reset --hard "#{sha1}" > /dev/null`
            break
        end
    end
end

def reset 
    `git fetch >/dev/null 2>/dev/null`
    `git reset --hard origin/master >/dev/null`
end


# Set up repo
local_path="./#{params[0]}"

if  params[0] == "" then
    puts "Using existing repository at #{local_path}"
    `cd "#{local_path}"`
else
    puts "Cloning repository to #{local_path}"
    `git clone "#{params[0]}" "#{local_path}"`
    `cd "#{local_path}"`
end


while true do
    reset
    prepare_index
    solve
    if !`git push origin master` then
        puts "Success :)"
     break
    else
    puts "Starting over :("
    reset
    end
end