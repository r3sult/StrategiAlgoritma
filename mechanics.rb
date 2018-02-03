require 'io/console'

class Account
  def initialize(name,pin,address,balance,active)
    @name = name
    @pin = pin.to_i
    @address = address
    @balance = balance.to_i
    @active = active
    @log = []
  end

  def name
    @name
  end

  def pin
    @pin
  end

  def address
    @address
  end

  def balance
    @balance
  end

  def active
    @active
  end

  def mutation
    @log
  end

  def insertmutation(type, amount)
    @log.unshift("#{type.upcase}  #{amount}")
    @log.pop if @log.length > 5
  end

  def edit(x, data)
    case x
    when "name"
      @name = data
    when "pin"
      @pin = data
    when "address"
      @address = data
    when "balance"
      @balance = data
    when "active"
      @active = data
    else
    end
  end
end

@acc_data = Hash.new(nil)
@cur_acc = nil


def create_account
  loop do
    @acc = Random.rand(1000..9999)
    break if @acc_data[@acc.to_s.to_sym].nil?
  end
  @cur_acc=@acc.to_s.to_sym
  print "Name           : "
  name = gets.chomp
  print "PIN            : "
  pin = STDIN.noecho(&:gets).chomp
  puts
  print "Address        : "
  address = gets.chomp
  print "Initial Balance: "
  balance = gets.chomp
  @acc_data[@acc.to_s.to_sym] = Account.new(name,pin,address,balance,true)
  puts "Your account has been created with account number #{@acc}"
end

def admin_print_data
  @acc_data.each do |x,y|
    puts "----------------------------------------------------"
    puts "------------------Account no. #{x}------------------"
    puts "----------------------------------------------------"
    puts "Name      :  #{@acc_data[x].name}"
    puts "PIN Number:  #{@acc_data[x].pin}"
    puts "Address   :  #{@acc_data[x].address}"
    puts "Balance   :  Rp #{@acc_data[x].balance}"
    puts "Active    :  #{@acc_data[x].active}"
    puts "----------------------------------------------------"
  end
end

def print_mutation (acc)
    mutation = @acc_data[acc].mutation
    puts "----------------------------------------------------"
    puts "------------------Account no. #{acc.to_s}------------------"
    puts "----------------------------------------------------"
    if mutation.nil?
      puts "Account mutation empty!"
    else
      puts "From most recent: "
      mutation.each {|x| puts x}
    end
    puts "----------------------------------------------------"
end

def print_data (acc)
  puts "----------------------------------------------------"
  puts "------------------Account no. #{acc.to_s}------------------"
  puts "----------------------------------------------------"
  puts "Name      :  #{@acc_data[acc].name}"
  puts "PIN Number:  #{@acc_data[acc].pin}"
  puts "Address   :  #{@acc_data[acc].address}"
  puts "Balance   :  Rp #{@acc_data[acc].balance}"
  puts "Active    :  #{@acc_data[acc].active}"
  puts "----------------------------------------------------"
end

def edit_data (acc)
  print_data(acc)
  puts
  loop do
    puts "Which data do you want to edit? "
    puts "| NAME  PIN  ADDRESS |"
    print ">> "
    input = gets.chomp.downcase

    case input
      when "name"
        puts "Insert your new name"
        print ">> "
        input1 = gets.chomp.capitalize
        @acc_data[acc].edit(input, input1)
        puts "Name successfuly changed to #{input1}!"

      when "pin"
        loop do
          puts "Insert your new PIN"
          print ">> "
          input1 = Integer(gets.chomp) rescue false
          break if input1
          puts "Invalid input!"
        end
        @acc_data[acc].edit(input, input1)
        puts "PIN successfuly changed to #{input1}!"

      when "address"
        puts "Insert your new address "
        print ">> "
        input1 = gets.chomp.capitalize
        @acc_data[acc].edit(input, input1)
        puts "Address successfuly changed to #{input1}"

      else
        puts "Invalid input!"
    end
    break if input == "name" || input == "pin" || input == "address"
  end
end


def block_account (acc)
  @acc_data[acc].edit("active", false)
end


def add_balance(noacc)
  print "Balance : "
  loop do
    @addbalance = Integer(gets.chomp) rescue false
    break if @addbalance
    puts "Invalid input"
  end
  @acc_data[noacc].edit("balance",(@acc_data[noacc].balance + @addbalance))
  @acc_data[noacc].insertmutation("K",@addbalance)
  puts "Success, Balance : #{@acc_data[noacc].balance}"
end


def withdraw_balance(noacc)
  loop do
    print "Balance : "
    loop do
      @withdraw = Integer(gets.chomp) rescue false
      break if @withdraw
      puts "Invalid input"
    end
    break if @withdraw <= @acc_data[noacc].balance
    puts "Balance isn't enough"
  end
  @acc_data[noacc].edit("balance",(@acc_data[noacc].balance - @withdraw))
  @acc_data[noacc].insertmutation("D",@withdraw)
  puts "Withdraw success"
end


def login
  chance =Hash.new(3)
  loop do
    loop do
      print "No. Acc : "
      @noacc = Integer(gets.chomp) rescue false
      break if @noacc && !@acc_data[@noacc.to_s.to_sym].nil?
      puts "Invalid account number"
    end
    if @acc_data[@noacc.to_s.to_sym].active
      print "PIN : "
      pin = Integer(gets.chomp) rescue false
      break if pin==@acc_data[@noacc.to_s.to_sym].pin
      chance[@noacc.to_s.to_sym] -= 1
      if chance[@noacc.to_s.to_sym]==0
        puts "Account is blocked"
        @acc_data[@noacc.to_s.to_sym].active=false
      else
        puts "Invalid pin, Chance remaining : #{chance[@noacc.to_s.to_sym]}"
      end
    end
    break if !@acc_data[@noacc.to_s.to_sym].active
  end
  if chance[@noacc.to_s.to_sym]>0
    if @acc_data[@noacc.to_s.to_sym].active
      @cur_acc=@noacc.to_s.to_sym
      puts "Login success"
    else
      puts "Account is frozen"
      @cur_acc=nil
    end
  else
    puts "Login failed"
    @cur_acc = nil
  end
end

loop do
  puts "Welcome to Bukalapak Bank"
  puts "Menu"
  puts "1. Create"
  puts "2. Login"
  puts "3. Exit"
  loop do
    print ">> "
    @input = gets.chomp.downcase
    break if @input == "create"||@input=="exit" || @input == "login"
    puts "Invalid input"
  end
  if @input == "create"
    create_account
  elsif @input == "login"
    login
  end
  if (@cur_acc.nil?)
    "Exit..."
  else
    puts "Welcome #{@acc_data[@cur_acc].name}"
    loop do
      puts "Menu"
      puts "1. check"
      puts "2. mutation"
      puts "3. add"
      puts "4. withdraw"
      puts "5. edit"
      puts "6. freeze"
      puts "7. logout"
      puts "8. exit"
      loop do
        print ">> "
        @input2 = gets.chomp.downcase
        break if @input2=="freeze"||@input2=="check"||@input2=="mutation"||@input2=="add"||@input2=="withdraw"||@input2=="edit"||@input2=="logout"||@input2=="exit"
        puts "Invalid input"
      end
      case @input2
      when "check"
        print_data(@cur_acc)
      when "mutation"
        print_mutation(@cur_acc)
      when "add"
        add_balance(@cur_acc)
      when "edit"
        edit_data(@cur_acc)
      when "withdraw"
        withdraw_balance(@cur_acc)
      when "freeze"
        block_account(@cur_acc)
        @input2="logout"
      else
        @cur_acc=nil
      end
      break if @input2=="exit" || @input2 =="logout"
    end
  end
  break if @input=="exit" || @input2=="exit"
end
