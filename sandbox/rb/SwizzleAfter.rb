# tests to verify the student's code
if (defined?(var)).nil?
  passing("declared myString", nil)
  if myString.is_a? String
    passing("myString is the correct type", nil)
    if myString == "my first ruby quiz"
      passing("myString has the correct value", nil)
    else
      failing("incorrect value", nil)
    end
  else
    failing("not a string", nil)
  end
else
  failing("not delcared", nil)
end
