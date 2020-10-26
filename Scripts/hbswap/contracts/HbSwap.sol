pragma solidity ^0.5.0;

contract HbSwap {
    event Inputmask(address user, uint idxETH, uint idxTOK);
    event Trade(address user, uint maskedETH, uint maskedTOK);

    uint public inputmaskCnt;

    constructor() public {}

    function tradePrep() public {
        emit Inputmask(msg.sender, inputmaskCnt, inputmaskCnt + 1);

        inputmaskCnt += 2;
    }

    function trade(uint maskedETH, uint maskedTOK) public {
        emit Trade(msg.sender, maskedETH, maskedTOK);
    }

}
