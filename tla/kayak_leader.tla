--------------------------------- MODULE kayak_leader ---------------------------------
\* A specification for leader behavior in Kayak.
\*
\* https://github.com/ericlee123/kayak

EXTENDS Naturals, FiniteSets, Sequences, TLC

\* The set of keys that can go into the log
CONSTANTS Key

\* The set of values that can go into the log
CONSTANTS Value

\* A reserved value.
CONSTANTS Nil

----
\* Global variables

\* A history variable used in the proof. This would not be present in an
\* implementation.
\* Keeps track of every log ever in the system (set of logs).
VARIABLE allLogs

----
\* Leader node variables

\* A Sequence of log entries. The index into this sequence is the index of the
\* log entry. Unfortunately, the Sequence module defines Head(s) as the entry
\* with index 1, so be careful not to use that!
VARIABLE log

\* The index of the latest entry in the log the state machine may apply.
VARIABLE commitIndex

\* Locks meant for shared access/modification. A thread should first obtain an
\* exclusive lock in one before grabbing a shared lock in the other.
VARIABLE access_locks
VARIABLE modify_locks

\* Current batch of minitransactions
VARIABLE concurrentMT

----

\* All variables; used for stuttering (asserting state hasn't changed).
vars == <<allLogs, log, commitIndex, access_locks, modify_locks, concurrentMT>>

----
\* Helpers

\* Return the minimum value from a set, or undefined if the set is empty.
Min(s) == CHOOSE x \in s : \A y \in s : x <= y
\* Return the maximum value from a set, or undefined if the set is empty.
Max(s) == CHOOSE x \in s : \A y \in s : x >= y    

InidicesWithKey(curLog, key) == { i \in (1..Len(curLog)) : key \in DOMAIN curLog[i] }

Compare(curLog, key, value) ==
    IF Len(log) > 0 /\ curLog[Max(InidicesWithKey(curLog, key))][key] = value
    THEN TRUE
    ELSE FALSE

\*Truncate(curLog, length) ==

----
\* Define initial values for all variables

Init == /\ allLogs      = {}
        /\ log          = <<[ i \in Key |-> 0 ]>>
        /\ commitIndex  = 0
        /\ concurrentMT = {}
        /\ access_locks = [k \in Key |-> 0]
        /\ modify_locks = [k \in Key |-> 0]

----
\* Define state transitions

\* On restart, all locks and everything are reset; log is truncated to last committed index
Restart(z) ==
    /\ access_locks' = [k \in Key |-> 0]
    /\ modify_locks' = [k \in Key |-> 0]
    /\ concurrentMT' = {}
    /\ UNCHANGED <<commitIndex, log>> \* TODO: need to reset log

\* Leader receives minitransaction request from client
ReceiveMinitransaction(cs, ws, rs) ==
    /\ \A k \in DOMAIN cs : modify_locks[k] = 0
    /\ \A k \in DOMAIN ws : access_locks[k] = 0
    /\ \A k \in rs        : access_locks[k] = 0
    /\ access_locks' = [ k \in DOMAIN access_locks |-> IF k \in (DOMAIN cs \union rs) \ DOMAIN ws THEN access_locks[k] + 1 ELSE access_locks[k] ]
    /\ modify_locks' = [ k \in DOMAIN modify_locks |-> IF k \in DOMAIN ws THEN modify_locks[k] + 1 ELSE modify_locks[k] ]
    /\ LET wat == <<cs>>
           huh == Append(wat, ws)
           mt  == Append(huh, rs)
       IN concurrentMT' = concurrentMT \union {mt}
    /\ UNCHANGED <<log, commitIndex>>
    
ProcessMinitransaction(mt) ==
    /\ LET cs == mt[1]
           ws == mt[2]
           rs == mt[3]
       IN IF \A k \in DOMAIN cs : Compare(log, k, cs[k]) THEN log' = Append(log, ws) ELSE UNCHANGED <<log>>
    /\ access_locks' = [ k \in DOMAIN access_locks |-> IF k \in (DOMAIN mt[1] \union mt[3]) \ DOMAIN mt[2] THEN access_locks[k] - 1 ELSE access_locks[k] ]
\*    /\ modify_locks' = [ k \in DOMAIN modify_locks |-> IF k \in DOMAIN mt[2] THEN modify_locks[k] - 1 ELSE modify_locks[k] ]
    /\ concurrentMT' = concurrentMT \ {mt}
    /\ UNCHANGED <<commitIndex, modify_locks>>

AdvanceCommitIndex(z) ==
    /\ LET newCommitIndex == Min({commitIndex + 1, Len(log) - 1})
       IN commitIndex' = newCommitIndex
       /\ modify_locks' = IF newCommitIndex > 0
                          THEN [ k \in DOMAIN modify_locks |-> IF k \in DOMAIN log[newCommitIndex] THEN modify_locks[k] - 1 ELSE modify_locks[k] ]
                          ELSE modify_locks
    /\ UNCHANGED <<log, concurrentMT, access_locks>>

----
\* Defines how the variables may transition.
Next == /\ \/ Restart(0)
           \/ ReceiveMinitransaction([ i \in Key |-> 0 ], [ i \in Key |-> 0 ], {})
           \/ \E mt \in concurrentMT : ProcessMinitransaction(mt)
           \/ AdvanceCommitIndex(0)
        /\ allLogs' = allLogs \union {log}

\* The specification must start with the initial state and transition according
\* to Next.
Spec == Init /\ [][Next]_vars

===============================================================================
